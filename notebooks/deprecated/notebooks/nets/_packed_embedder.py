from torch.nn import Module
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence, PackedSequence


class PackedEmbedder(Module):
    def __init__(self, embedder):
        """Initialize a PackedEmbedder"""
        super().__init__()
        self.embedder = embedder
        self.padding_value = embedder.padding_idx or 0

    def forward(self, x):
        """Embed :param x, which may either be a packed sequence or a normal tensor."""
        if isinstance(x, PackedSequence):
            # Unpack first, then repack afterwards.
            x, lengths = pad_packed_sequence(x, padding_value=self.padding_value)

            return pack_padded_sequence(self.embedder(x), lengths, enforce_sorted=False)

        return self.embedder(x)
