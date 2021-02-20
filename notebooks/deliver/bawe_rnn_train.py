from datetime import datetime
import os
from os.path import join
from pathlib import Path
import pickle
import sys
import torch
from torch import optim
from torch.nn import Embedding
from torch.nn.functional import mse_loss
from torch.utils.data import TensorDataset
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

sys.path.append(os.path.abspath(Path('..')))

from notebooks.datatools import EqualOpDataLoader, Preprocessor  # noqa
from notebooks.nets import EuclideanDiscriminator, PackedEmbedder, ParEncoder, SentenceEncoder, StyleEncoder  # noqa

writer_dir = Path('../runs')

dev = torch.device(0)
writer = SummaryWriter(join(writer_dir, f'{datetime.now()}-bawe-par-encoder'))

preprocessed_data_dir = Path('../data/preprocess')
resources_dir = Path('../resources')

train_data = torch.load(join(preprocessed_data_dir, 'bawe_train_data.pt'))
train_sentence_lengths = torch.load(join(preprocessed_data_dir,
                                         'bawe_train_sentence_lengths.pt'))
train_labels = torch.load(join(preprocessed_data_dir, 'bawe_train_labels.pt'))

valid_data = torch.load(join(preprocessed_data_dir, 'bawe_valid_data.pt'))
valid_sentence_lengths = torch.load(join(preprocessed_data_dir,
                                         'bawe_valid_sentence_lengths.pt'))
valid_labels = torch.load(join(preprocessed_data_dir, 'bawe_valid_labels.pt'))

with open(join(resources_dir, 'pos_vocab.p'), 'rb') as f:
    pos_vocab = pickle.load(f)

train_set = TensorDataset(train_data, train_sentence_lengths, train_labels)
valid_set = TensorDataset(valid_data, valid_sentence_lengths, valid_labels)

embedder = PackedEmbedder(Embedding(len(pos_vocab), 100,
                                    padding_idx=pos_vocab['<pad>']))
sentence_encoder = SentenceEncoder(100, 100)
par_encoder = ParEncoder(100, 100)

style_encoder = StyleEncoder(embedder, sentence_encoder, par_encoder).to(dev)
style_discriminator = EuclideanDiscriminator().to(dev)

torch.seed()

# Hyperparameters
batch_count = 1000
lr = 1e-6
opt = optim.SGD([{'params': style_discriminator.parameters()},
                 {'params': style_encoder.parameters()}], lr=lr)
criterion = mse_loss
bs = 75

preprocessor = Preprocessor(dev)
train_dl = EqualOpDataLoader(train_set, bs=bs, collate_fn=preprocessor)
valid_dl = EqualOpDataLoader(valid_set, bs=bs, collate_fn=preprocessor)


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

fit()

outputs_dir = Path('../outputs')
if not os.path.isdir(outputs_dir):
    os.mkdir(outputs_dir)

torch.save(style_encoder.state_dict(),
           join(outputs_dir, 'bawe_style_encoder_sd.pt'))
torch.save(style_discriminator.state_dict(),
           join(outputs_dir, 'bawe_style_discriminator_sd.pt'))

writer.close()
