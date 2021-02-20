import torch
from torch import Tensor
from torch.nn import Module
from torch.nn.utils.rnn import PackedSequence, pad_packed_sequence


class Seq2Vec(Module):
    """A sequence-to-vector RNN."""

    def __init__(self, rnn, attn=None):
        """
        Initialize a Seq2Vec module.

        :param rnn: The RNN module to use for encoding.
        :param attn: The attention module to use after encoding.
        """
        super().__init__()

        if attn is None:
            self._impl = NoAttnSeq2Vec(rnn)
        else:
            self._impl = AttnSeq2Vec(rnn, attn)

    def forward(self, x):
        """
        Pass :param x through the network.

        :param x: The input for the network, should be of shape (seq_len, batch_size, num_features). If attention is
        used, this should not be a packed sequence.

        :return: The output of the network.
        """
        return self._impl(x)


class NoAttnSeq2Vec(Module):
    """A sequence-to-vector RNN, without attention."""

    def __init__(self, rnn):
        """
        Initialize a NoAttnSeq2Vec module.

        :param rnn: The RNN module to use in encoding.
        """
        super().__init__()
        self.rnn = rnn

    def forward(self, x: Tensor) -> Tensor:
        """
        Pass :param x through the network.

        :param x: The input to the network, should be of shape (seq_len, batch_size, num_features).

        :return: The output of the network.
        """
        encoding, _ = self.rnn(x)

        # The way that we retrieve the last encoding depends on whether the sequence is packed.
        if isinstance(encoding, PackedSequence):
            encoding, seq_lens = pad_packed_sequence(encoding)

            # If the sequence is packed, then each encoding is at the position of the last item in the sequence
            # (seq_len - 1).
            encoding = encoding[seq_lens - 1, torch.arange(encoding.shape[1])]
        else:
            # If the sequence is not packed, then we know each encoding is simply located at the last position in the
            # sequence.
            encoding = encoding[-1]

        return encoding


class AttnSeq2Vec(Module):
    """A sequence-to-vector RNN, with attention. Does not support packed tensors"""

    def __init__(self, rnn, attn):
        """
        Initialize an AttnSeq2Vec module.

        :param rnn: The RNN module to use in encoding.
        :param attn: The attention module to use after encoding.
        """
        super().__init__()
        self.rnn = rnn
        self.attn = attn

    def forward(self, x):
        """
        Pass :param x through the network.

        :param x: The input to the network, should be of shape (seq_len, batch_size, num_features). Packed tensors are
        not supported.

        :return: The output of the network.
        """
        seq_outputs, _ = self.rnn(x)

        encoding = self.attn(seq_outputs)

        return encoding
