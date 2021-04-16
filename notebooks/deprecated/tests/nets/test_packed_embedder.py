from unittest.mock import MagicMock

import pytest
import torch
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence

from notebooks.nets._packed_embedder import PackedEmbedder


def mock_embed(tensor):
    num_dims = len(tensor.shape)
    new_dim = num_dims

    return torch.repeat_interleave(tensor.unsqueeze(new_dim), 5, new_dim)


mock_embedding = MagicMock(side_effect=mock_embed)
mock_embedding.forward = mock_embed
mock_embedding.padding_idx = None


def get_last_items(sequence, seq_lengths):
    return sequence[seq_lengths - 1, torch.arange(sequence.shape[1])]


class TestPackedEmbedder:
    padded_tensors = [torch.tensor([[1, 2, 1], [2, 0, 1], [0, 0, 1], [0, 0, 2]])]

    padded_tensor_lengths = [torch.tensor([2, 1, 4])]

    padded_tensor_last_items = [
        torch.tensor([[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]])
    ]

    @pytest.mark.parametrize("x, lengths", zip(padded_tensors, padded_tensor_lengths))
    def test_packed_embedder_retains_shape(self, x, lengths):
        packed_x = pack_padded_sequence(x, lengths, enforce_sorted=False)
        embedder = PackedEmbedder(mock_embedding)

        embedding = embedder(packed_x)
        unpacked_embedding, _ = pad_packed_sequence(embedding)

        expected_shape = (*x.shape, 5)
        assert unpacked_embedding.shape == expected_shape

    @pytest.mark.parametrize(
        "x, lengths, expected_last_items",
        zip(padded_tensors, padded_tensor_lengths, padded_tensor_last_items),
    )
    def test_packed_embedder_retains_position(self, x, lengths, expected_last_items):
        packed_x = pack_padded_sequence(x, lengths, enforce_sorted=False)
        embedder = PackedEmbedder(mock_embedding)

        unpacked_embedding, _ = pad_packed_sequence(embedder(packed_x))

        assert torch.all(
            torch.eq(get_last_items(unpacked_embedding, lengths), expected_last_items)
        )

    tensors = [torch.tensor([[1, -1, 5], [2, -2, 6], [3, -3, 7], [4, -4, 8]])]

    @pytest.mark.parametrize("x", tensors)
    def test_packed_embedder_accepts_normal_tensors(self, x):
        embedder = PackedEmbedder(mock_embedding)

        embedding = embedder(x)

        assert torch.all(torch.eq(embedding, mock_embedding(x)))
