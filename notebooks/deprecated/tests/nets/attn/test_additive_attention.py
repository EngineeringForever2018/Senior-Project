import pytest
import torch

from notebooks.nets.attn._additive_attention import AdditiveAttention


class TestAdditiveAttention:
    test_data = [(torch.ones(5, 7, 8), 8, (7, 8)), (torch.ones(6, 4, 3), 3, (4, 3))]

    @pytest.mark.parametrize("x, encoding_dim, expected_shape", test_data)
    def test_attn_shape(self, x, encoding_dim, expected_shape):
        attn = AdditiveAttention(encoding_dim)

        output = attn(x)

        assert output.shape == expected_shape
