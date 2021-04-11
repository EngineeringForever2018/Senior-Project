import torch
from torch.nn import Module, Linear
from torch.nn.functional import softmax


class AdditiveAttention(Module):
    """An additive attention module."""

    def __init__(self, encoding_dim):
        """
        Initialize an AdditiveAttention module.

        :param encoding_dim: The dimensionality of encoding vectors.
        """
        super().__init__()
        self.encoder_module = Linear(encoding_dim, encoding_dim, bias=False)
        self.alignment_module = Linear(encoding_dim, 1, bias=False)

    def forward(self, encoder_outputs):
        """
        Find the context vector for the given :param encoder_outputs

        :param encoder_outputs: A tensor of shape (seq_len, batch_size, encoding_dim) that represents the encoding
        outputs from an RNN.

        :return: The context vectors of shape (batch_size, encoding_dim).
        """
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
