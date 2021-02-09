import torch
from torch.nn import Linear, LSTM, Module
from torch.nn.functional import softmax
from torch.nn.utils.rnn import pad_packed_sequence


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
        encoding, _ = self.encoder(x)

        encoding, sent_lens = pad_packed_sequence(encoding)

        encoding = encoding[sent_lens - 1, torch.arange(encoding.shape[1]), :]

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