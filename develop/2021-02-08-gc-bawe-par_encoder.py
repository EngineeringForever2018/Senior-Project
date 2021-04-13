import torch
import pickle
from tqdm import tqdm

torch.zeros(4)

# dev = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
dev = torch.device('cuda')

from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

writer = SummaryWriter(f'runs/{datetime.now()}-bawe-par-encoder')

labels = torch.load('../data/bawe-preprocess/labels.pt')
data = torch.load('../data/bawe-preprocess/data.pt')
sent_lens = torch.load('../data/bawe-preprocess/sent_lens.pt')

label_set = pickle.load(open('../data/bawe-preprocess/label_set.p', 'rb'))
bawe_train_stats = pickle.load(open('../data/bawe_train_stats.p', 'rb'))
max_sent_len = bawe_train_stats['max_sent_len']
pos_vocab = bawe_train_stats['pos_vocab']

torch.manual_seed(0)

order = torch.randperm(len(labels))

valid_size = int(len(order) / 5)

valid_indices = order[:valid_size]

valid_selection = torch.zeros(len(labels), dtype=bool)
valid_selection[valid_indices] = True

train_selection = torch.logical_not(valid_selection)

train_labels = labels[train_selection].contiguous()
train_data = data[train_selection].contiguous()
train_sent_lens = sent_lens[train_selection].contiguous()

valid_labels = labels[valid_selection].contiguous()
valid_data = data[valid_selection].contiguous()
valid_sent_lens = sent_lens[valid_selection].contiguous()

train_label_set = sorted(list(set([int(label) for label in train_labels])))
valid_label_set = sorted(list(set([int(label) for label in valid_labels])))

train_label_set = torch.tensor(train_label_set)
valid_label_set = torch.tensor(valid_label_set)

from torch.utils.data import TensorDataset

train_set = TensorDataset(train_data, train_sent_lens, train_labels)
valid_set = TensorDataset(valid_data, valid_sent_lens, valid_labels)

class EqualOpDataLoader:
    def __init__(self, dataset, label_set, bs=1):
        self.dataset = dataset
        _, _, self.labels = dataset[:]
        self.label_set = label_set
        self.bs = bs
    
    def __iter__(self):
        bs = self.bs
        for _ in range(int(len(self.dataset) / bs)):
            order = torch.randperm(len(self.label_set))
            
            first_labels = self.label_set[order[:bs]]
            second_labels = first_labels
            
            different_selection = torch.bernoulli(torch.full([bs], 0.5)).to(bool)
            different_labels = self.label_set[order[bs:2*bs]]
            
            second_labels[different_selection] = different_labels[different_selection]
            
            def sample_label(label):
                selection = (self.labels == label)
                
                dataset_selection = self.dataset[selection]
                
                data_, sent_lens_, labels_ = dataset_selection
                
                selected_index = torch.randint(high=len(labels_), size=(1,))
                
                return data_[selected_index:selected_index+1], sent_lens_[selected_index:selected_index+1], labels_[selected_index:selected_index+1]
            
            def samples(chosen_labels):
                result = [sample_label(label) for label in chosen_labels]
                
                data_, sent_lens_, labels_ = zip(*result)
                
                data_ = torch.cat(data_, dim=0)
                sent_lens_ = torch.cat(sent_lens_, dim=0)
                labels_ = torch.cat(labels_, dim=0)
                
                return data_, sent_lens_, labels_
            
            first_data, first_sent_lens, first_labels = samples(first_labels)
            second_data, second_sent_lens, second_labels = samples(second_labels)
            
            yield first_data, first_sent_lens, first_labels, second_data, second_sent_lens, second_labels
    
    def __len__(self):
        return int(len(self.dataset) / self.bs)

from torch.nn.utils.rnn import pack_padded_sequence

class GPUDataLoader:
    def __init__(self, dl, embedding, dev):
        self.dl = dl
        self.embedding = embedding
        self.dev = dev
    
    def __iter__(self):
        for first_data, first_sent_lens, first_labels, second_data, second_sent_lens, second_labels in self.dl:
            first_data, second_data = self.embedding(first_data).to(self.dev), self.embedding(second_data).to(self.dev)
            
            def reform(data_, sent_lens_):
                batch_size, _, seq_len, embedding_dim = data_.size()
                
                # (4 * batch_size, seq_len, embedding_dim)
                reshaped = torch.reshape(data_, [-1, seq_len, embedding_dim])
                
                return torch.transpose(reshaped, 0, 1), torch.reshape(sent_lens_, [-1])
            
            first_data, first_sent_lens = reform(first_data, first_sent_lens)
            second_data, second_sent_lens = reform(second_data, second_sent_lens)
            
            first_data = pack_padded_sequence(first_data, first_sent_lens, enforce_sorted=False)
            second_data = pack_padded_sequence(second_data, second_sent_lens, enforce_sorted=False)
            
            yield first_data, first_labels, second_data, second_labels
    
    def __len__(self):
        return len(self.dl)

from torch.nn import Linear, LSTM, Module
from torch.nn.functional import softmax
from torch.nn.utils.rnn import pad_packed_sequence, PackedSequence

class BahdanauAttention(Module):
    def __init__(self, encoding_dim):
        super().__init__()
        self.encoder_module = Linear(encoding_dim, encoding_dim, bias=False)
        self.alignment_module = Linear(encoding_dim, 1, bias=False)
    
    def forward(self, encoder_outputs):
        # (seq_len, batch_size, encoder_size) -> (batch_size, seq_len, encoder_size)
        encoder_outputs = torch.transpose(encoder_outputs, 0, 1)
        
        # (batch_size, seq_len, encoder_size)
        encoder_activations = (self.encoder_module(encoder_outputs))
        # (batch_size, seq_len, encoder_size) -> (batch_size, seq_len, 1)
        alignment_scores = self.alignment_module(torch.tanh(encoder_activations))
        
        attn_weights = softmax(alignment_scores, dim=1)
        
        # (batch_size, encoder_size, seq_len)
        encoder_outputs = torch.transpose(encoder_outputs, 1, 2)
        # (batch_size, encoder_size, seq_len) X (batch_size, seq_len, 1) -> (batch_size, encoder_size, 1)
        context_vectors = torch.bmm(encoder_outputs, attn_weights)
        
        return context_vectors.squeeze(2)

class SentenceEncoder(Module):
    def __init__(self, embedding_dim, encoding_dim):
        super().__init__()
        self.encoder = LSTM(embedding_dim, encoding_dim)
    
    def forward(self, x):
        encoding, _= self.encoder(x)
        
        if isinstance(encoding, PackedSequence):
            encoding, sent_lens = pad_packed_sequence(encoding)

            encoding = encoding[sent_lens - 1, torch.arange(encoding.shape[1]), :]
        else:
            encoding = encoding[-1]

        return torch.reshape(encoding, [4, -1, encoding.shape[1]])

class ParEncoder(Module):
    def __init__(self, sent_encoding_dim, encoding_dim):
        super().__init__()
        self.encoder = LSTM(sent_encoding_dim, encoding_dim)
        self.attention = BahdanauAttention(encoding_dim)
    
    def forward(self, x):
        encoding, _ = self.encoder(x)
        
        return self.attention(encoding)

class StyleEncoder(Module):
    def __init__(self, sentence_encoder, par_encoder):
        super().__init__()
        self.sentence_encoder = sentence_encoder
        self.par_encoder = par_encoder
    
    def forward(self, x):
        sentence_encoding = self.sentence_encoder(x)
        
        return self.par_encoder(sentence_encoding)

class EuclideanDiscriminator(Module):
    def __init__(self):
        super().__init__()
        self.linear = Linear(1, 1)
        
    def forward(self, x1, x2):
        diff = x1 - x2
        
        distance = torch.sqrt(torch.sum(diff * diff, dim=1))
        
        probability = torch.sigmoid(self.linear(distance.unsqueeze(1)))
        
        return probability

from torch.nn import Embedding

embedding = Embedding(len(pos_vocab), 10, padding_idx=pos_vocab['<pad>'])
sentence_encoder = SentenceEncoder(10, 10).to(dev)
par_encoder = ParEncoder(10, 5).to(dev)

style_encoder = StyleEncoder(sentence_encoder, par_encoder).to(dev)
style_discriminator = EuclideanDiscriminator().to(dev)

class CombinedModel(Module):
    def __init__(self, style_encoder_, style_discriminator_):
        super().__init__()
        self.style_encoder = style_encoder_
        self.style_discriminator = style_discriminator_
    
    def forward(self, x1, x2):
        x1_encoding = self.style_encoder(x1)
        x2_encoding = self.style_encoder(x2)
        
        return self.style_discriminator(x1_encoding, x2_encoding)

combined = CombinedModel(style_encoder, style_discriminator)
    
writer.add_graph(combined, (torch.zeros([24, 80, 10]).to(dev), torch.zeros([24, 80, 10]).to(dev)))
writer.flush()

from torch import optim
from torch.nn.functional import mse_loss
from torch.utils.data import DataLoader

torch.seed()

# Hyperparameters
epochs = 1
lr = 1e-3
opt = optim.Adam([{'params': style_discriminator.parameters()}, {'params': style_encoder.parameters()}, {'params': embedding.parameters()}])
criterion = mse_loss
bs = 75

train_dl = GPUDataLoader(EqualOpDataLoader(train_set, train_label_set, bs=bs), embedding, dev)
valid_dl = GPUDataLoader(EqualOpDataLoader(valid_set, valid_label_set, bs=bs), embedding, dev)

from tqdm import tqdm

torch.seed()


def fit(validate=True):
    for epoch in range(epochs):
        for index, (x1b, y1b, x2b, y2b) in tqdm(enumerate(train_dl), total=len(train_dl)):
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

            if index % 100 == 0:
                valid_loss, valid_accuracy = evaluate(valid_dl, give_acc=True)
                writer.add_scalar('Validation Loss', valid_loss, index)
                writer.add_scalar('Validation Accuracy', valid_accuracy, index)

            if index == 900:
                break
        break
#         train_loss = evaluate(train_eval_dl)
#         writer.add_scalar('Training Loss', train_loss, epoch)
        if validate:
            valid_loss, valid_accuracy = evaluate(valid_dl, give_acc=True)
            writer.add_scalar('Validation Loss', valid_loss, epoch)
            writer.add_scalar('Validation Accuracy', valid_accuracy, epoch)
#             writer.add_scalar('Validation Accuracy', valid_accuracy, epoch)

        writer.flush()


def y_difference(y1, y2):
    return torch.logical_not((y1 == y2)).to(dtype=int).to(dev)


def evaluate(dl, give_acc=False):
    with torch.no_grad():
        preds_y = [(style_discriminator(style_encoder(x1b),
                                        style_encoder(x2b)),
                    y_difference(y1b, y2b))
                   for x1b, y1b, x2b, y2b in dl]

        losses = [criterion(preds_b.squeeze(1), yb) for preds_b, yb in preds_y]
        loss = sum(losses) / len(losses)

        if give_acc:
            accs = [accuracy(preds_b, yb) for preds_b, yb in preds_y]
            acc = sum(accs) / len(accs)

            return loss, acc

        return loss


def accuracy(out, y):
    preds = out > 0.999
    return (preds == y).float().mean()

# torch.save(embedding.state_dict(), '../resources/bawe_embedding_sd.pt')
# torch.save(style_encoder.state_dict(), '../resources/bawe_style_encoder_sd.pt')
# torch.save(style_discriminator.state_dict(), '../resources/bawe_style_discriminator_sd.pt')

writer.flush()

fit()

writer.close()
