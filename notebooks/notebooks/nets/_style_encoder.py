import torch
from torch.nn import Module, LSTM

from notebooks.nets.attn import AdditiveAttention
from notebooks.nets import Seq2Vec


class StyleEncoder(Module):
    def __init__(self, packed_embedder, sentence_encoder, par_encoder):
        super().__init__()
        self.packed_embedder = packed_embedder
        self.sentence_encoder = sentence_encoder
        self.par_encoder = par_encoder

    def forward(self, x):
        pos_embedding = self.packed_embedder(x)

        sentence_encoding = self.sentence_encoder(pos_embedding)

        sentence_encoding = torch.reshape(sentence_encoding, [4, -1, sentence_encoding.shape[1]])

        return self.par_encoder(sentence_encoding)


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
