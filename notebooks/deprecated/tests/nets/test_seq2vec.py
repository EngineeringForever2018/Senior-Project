from unittest.mock import MagicMock

import pytest
import torch
from torch import Tensor
from torch.nn.utils.rnn import pack_padded_sequence

from notebooks.nets._seq2vec import NoAttnSeq2Vec, AttnSeq2Vec


def mock_forward(x):
    return x, 2


mock_rnn = MagicMock(side_effect=mock_forward)
mock_rnn.forward = mock_forward


def mock_attn_forward(x):
    return torch.mean(x, dim=0)


mock_attn = MagicMock(side_effect=mock_attn_forward)
mock_attn.forward = mock_attn_forward


class TestNoAttnSeq2Vec:
    normal_tensors = [
        (
            torch.tensor([[0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 2, 3]]),
            torch.tensor([1, 2, 3]),
        ),
        (
            torch.tensor(
                [[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0], [5.0, 4.0, 3.0, 2.0]]
            ),
            torch.tensor([5.0, 4.0, 3.0, 2.0]),
        ),
        (
            torch.repeat_interleave(
                torch.tensor([[0, 0, 0, 0], [1, 1, 1, 1], [1, 2, 3, 4]]).unsqueeze(2),
                3,
                dim=2,
            ),
            torch.tensor([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]),
        ),
    ]

    @pytest.mark.parametrize("x, expected", normal_tensors)
    def test_encoder_should_retrieve_last_seq_item(self, x: Tensor, expected: Tensor):
        encoder = NoAttnSeq2Vec(mock_rnn)

        output = encoder(x)

        assert torch.all(torch.eq(output, expected))

    packed_tensors = [
        (
            pack_padded_sequence(
                torch.tensor([[0, 0, 0], [1, 0, 0], [0, 0, 3], [0, 2, 0]]),
                torch.tensor([2, 4, 3]),
                enforce_sorted=False,
            ),
            torch.tensor([1, 2, 3]),
        ),
        (
            pack_padded_sequence(
                torch.tensor(
                    [[1.0, 4.0, 1.0, 1.0], [1.0, 0.0, 3.0, 1.0], [5.0, 0.0, 0.0, 2.0]]
                ),
                torch.tensor([3, 1, 2, 3]),
                enforce_sorted=False,
            ),
            torch.tensor([5.0, 4.0, 3.0, 2.0]),
        ),
        (
            pack_padded_sequence(
                torch.repeat_interleave(
                    torch.tensor([[0, 0, 0, 0], [0, 0, 3, 4], [1, 2, 0, 0]]).unsqueeze(
                        2
                    ),
                    2,
                    dim=2,
                ),
                torch.tensor([3, 3, 2, 2]),
                enforce_sorted=False,
            ),
            torch.tensor([[1, 1], [2, 2], [3, 3], [4, 4]]),
        ),
    ]

    @pytest.mark.parametrize("x, expected", packed_tensors)
    def test_encoder_should_retrieve_last_packed_seq_item(self, x, expected):
        encoder = NoAttnSeq2Vec(mock_rnn)

        output = encoder(x)

        assert torch.all(torch.eq(output, expected))


class TestAttnSeq2Vec:
    test_data = [
        (torch.tensor([[2, -2, 3.0], [4.0, 2.0, 6.0]]), torch.tensor([3.0, 0.0, 4.5])),
        (
            torch.repeat_interleave(
                torch.tensor([[1.0, 6.0, -9.0], [3.0, 8.0, 9.0]]).unsqueeze(2), 4, dim=2
            ),
            torch.tensor(
                [[2.0, 2.0, 2.0, 2.0], [7.0, 7.0, 7.0, 7.0], [0.0, 0.0, 0.0, 0.0]]
            ),
        ),
    ]

    @pytest.mark.parametrize("x, expected", test_data)
    def test_sec2vec_uses_attn(self, x, expected):
        encoder = AttnSeq2Vec(mock_rnn, mock_attn)

        output = encoder(x)

        assert torch.all(torch.eq(output, expected))
