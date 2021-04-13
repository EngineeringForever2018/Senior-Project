from datetime import datetime
import os
from os.path import join
import pandas as pd
from pathlib import Path
import pickle
import spacy
import sys
import torch
from torch import optim
from torch.nn import Embedding, LSTM
from torch.nn.functional import mse_loss
from torch.utils.data import TensorDataset
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir  # noqa

from notebooks import pipes  # noqa
from notebooks.datatools import AuthorDataset, EqualOpDataLoader  # noqa
from notebooks.nets import EuclideanDiscriminator, PackedEmbedder, StyleEncoder, Seq2Vec  # noqa
from notebooks.utils import POSVocab  # noqa

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))

dev = torch.device(0)
nlp = spacy.load('en_core_web_sm')
pos_vocab = POSVocab()

writer_dir = join(project_root, 'runs')

writer = SummaryWriter(join(writer_dir, f'{datetime.now()}-bawe-par-encoder'))

reprocess = False

train_data_path = join(preprocess_path, 'bawe_train_sentences_tokenized.hdf5')
valid_data_path = join(preprocess_path, 'bawe_valid_sentences_tokenized.hdf5')

train_data_exists = os.path.exists(train_data_path)
valid_data_exists = os.path.exists(valid_data_path)

pipeline = pipes.POSTokenize(nlp=nlp, pos_vocab=pos_vocab, show_loading=True)

if not (train_data_exists and valid_data_exists) or reprocess:
    print('Processing...', flush=True)

    train_df = pd.read_hdf(join(preprocess_path, 'bawe_train_sentences.hdf5'))
    valid_df = pd.read_hdf(join(preprocess_path, 'bawe_valid_sentences.hdf5'))

    train_data = pipeline(train_df)
    valid_data = pipeline(valid_df)

    train_data.to_hdf(train_data_path, 'bawe_train_sentences_tokenized')
    valid_data.to_hdf(valid_data_path, 'bawe_valid_sentences_tokenized')
else:
    train_data = pd.read_hdf(train_data_path)
    valid_data = pd.read_hdf(valid_data_path)

train_data.loc[(28, 0, 1)]

num_sentences = 20

pipeline = pipes.GroupSentences(n=num_sentences)

train_data = pipeline(train_data)
valid_data = pipeline(valid_data)

train_set = AuthorDataset(train_data)
valid_set = AuthorDataset(valid_data)

embedder = PackedEmbedder(Embedding(len(pos_vocab), 10,
                                    padding_idx=pos_vocab['<pad>']))
sentence_encoder = Seq2Vec(LSTM(10, 5))

style_encoder = StyleEncoder(embedder, sentence_encoder).to(dev)
style_discriminator = EuclideanDiscriminator(n=num_sentences).to(dev)

torch.seed()

# Hyperparameters
batch_count = 1000
lr = 1e-6
opt = optim.SGD([{'params': style_discriminator.parameters()},
                 {'params': style_encoder.parameters()}], lr=lr)
criterion = mse_loss
bs = 75

pipeline = pipes.PackSequence(dev=dev)
train_dl = EqualOpDataLoader(train_set, bs=bs, pipeline=pipeline)
valid_dl = EqualOpDataLoader(valid_set, bs=bs, pipeline=pipeline)


def fit(validate=True, validate_every=100):
    train_dl.batch_count = batch_count
    for index, ((x1b, y1b), (x2b, y2b)) in tqdm(enumerate(train_dl),
                                                total=len(train_dl)):
        x1_encoding = style_encoder(x1b)
        x2_encoding = style_encoder(x2b)

        pred = style_discriminator(x1_encoding, x2_encoding).squeeze(1)

        yb = y_difference(y1b, y2b).to(dtype=torch.float)

        loss = criterion(pred, yb)

        loss.backward()

        opt.step()
        opt.zero_grad()

        writer.add_scalar('Training Loss', loss, index)
        writer.flush()

        if validate:
            if index % 100 == 0:
                valid_loss, valid_acc = evaluate(valid_dl, give_acc=True)
                writer.add_scalar('Validation Loss', valid_loss, index)
                writer.add_scalar('Validation Accuracy', valid_acc, index)
                writer.flush()


def y_difference(y1, y2):
    return torch.logical_not((y1 == y2)).to(dtype=int).to(dev)


def evaluate(dl, give_acc=False):
    with torch.no_grad():
        preds_y = [(style_discriminator(style_encoder(x1b),
                                        style_encoder(x2b)),
                    y_difference(y1b, y2b))
                   for (x1b, y1b), (x2b, y2b) in dl]

        losses = [criterion(preds_b.squeeze(1), yb) for preds_b, yb in preds_y]
        loss = sum(losses) / len(losses)

        if give_acc:
            accs = [accuracy(preds_b, yb) for preds_b, yb in preds_y]
            acc = sum(accs) / len(accs)

            return loss, acc

        return loss


def accuracy(out, y):
    preds = out > 0.5
    return (preds == y).float().mean()

fit(validate=False)

outputs_dir = join(project_root, 'outputs')
if not os.path.isdir(outputs_dir):
    os.mkdir(outputs_dir)

torch.save(style_encoder.state_dict(),
           join(outputs_dir, 'bawe_style_encoder_sd.pt'))
torch.save(style_discriminator.state_dict(),
           join(outputs_dir, 'bawe_style_discriminator_sd.pt'))

writer.close()
