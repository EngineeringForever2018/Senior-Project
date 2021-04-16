import torch
from torch.nn import Module, LSTM

from notebooks.nets.attn import AdditiveAttention
from notebooks.nets import Seq2Vec


class StyleEncoder(Module):
    def __init__(self, packed_embedder, sentence_encoder):
        super().__init__()
        self.packed_embedder = packed_embedder
        self.sentence_encoder = sentence_encoder

    def forward(self, x):
        pos_embedding = self.packed_embedder(x)

        return self.sentence_encoder(pos_embedding)


class ParEncoder(Module):
    def __init__(self, sentence_encoding_dim, encoding_dim):
        super().__init__()
        rnn = LSTM(sentence_encoding_dim, encoding_dim)
        # attn = AdditiveAttention(encoding_dim)

        self.encoder = Seq2Vec(rnn)

    def forward(self, x):
        return self.encoder(x)


class SentenceEncoder(Module):
    def __init__(self, pos_embedding_dim, encoding_dim):
        super().__init__()
        rnn = LSTM(pos_embedding_dim, encoding_dim)

        self.encoder = Seq2Vec(rnn)

    def forward(self, x):
        return self.encoder(x)
