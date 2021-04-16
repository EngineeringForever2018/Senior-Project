from notebooks.structures import (
    PaddedArray,
    padded_mean,
    EmptyListException,
    EmptyArrayException,
)
from tests import tutils
import numpy as np
import pytest


# TODO: Either support other dimensions than 3 or formalize the support for 3
#       dimensions.
# TODO: PaddedArray appears to work for any sequence, not just a list. This should be
#       formalized and tested.
class TestPaddedArray:
    array_sets = [
        [
            np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]),
            np.array(
                [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
            ),
        ],
        [
            np.array([[2.0, 2.0, 2.0, 2.0], [2.0, 2.0, 2.0, 2.0]]),
            np.array([[2.0, 2.0, 2.0, 2.0]]),
            np.array(
                [
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                ]
            ),
        ],
        np.array([[[2.0, 2.0], [2.0, 2.0]], [[2.0, 2.0], [2.0, 2.0]]]),
    ]

    expected_data_set = [
        np.array(
            [
                [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]],
                [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]],
            ]
        ),
        np.array(
            [
                [
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [2.0, 2.0, 2.0, 2.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                    [2.0, 2.0, 2.0, 2.0],
                ],
            ]
        ),
        np.array([[[2.0, 2.0], [2.0, 2.0]], [[2.0, 2.0], [2.0, 2.0]]]),
    ]

    @pytest.mark.parametrize(
        "arrays, expected_data", zip(array_sets, expected_data_set)
    )
    def test_class_should_pad_numpy_array(self, arrays, expected_data):
        padded_array = PaddedArray(arrays)

        assert np.array_equal(padded_array.data, expected_data)

    expected_length_sets = [np.array([2, 3]), np.array([2, 1, 4]), np.array([2, 2])]

    @pytest.mark.parametrize(
        "arrays, expected_lengths", zip(array_sets, expected_length_sets)
    )
    def test_padded_arrays_should_have_correct_lengths(self, arrays, expected_lengths):
        padded_array = PaddedArray(arrays)

        assert np.array_equal(padded_array.lengths, expected_lengths)


# TODO: In the case of non-padded numpy arrays the dimensions should be asserted.
class TestPaddedArrayEdgeCases:
    def test_padded_array_should_not_accept_empty_list(self):
        with pytest.raises(EmptyListException):
            _ = PaddedArray([])

    def test_padded_array_should_not_accept_empty_arrays(self):
        with pytest.raises(EmptyArrayException):
            _ = PaddedArray([np.zeros([2, 4]), np.zeros([0, 4])])


# TODO: Decide how edge cases of empty arrays should be handled
class TestPaddedMean:
    padded_arrays = [
        PaddedArray(
            [
                np.array([[4.0, -5.0, 0.0, 0.0], [2.0, 2.0, -3.0, 0.0]]),
                np.array(
                    [[1.0, 2.0, 3.0, 4.0], [4.0, 3.0, 2.0, 1.0], [2.0, 2.0, 2.0, 2.0]]
                ),
            ]
        ),
        PaddedArray(
            [
                np.array([[1.0, 9.0], [4.3, 5.2], [-2.2, -4.4], [11.0, 12.0]]),
                np.array([[5.6, 0.2], [0.3, 0.6]]),
            ]
        ),
    ]

    expected_mean_sets = [
        np.array([[3.0, -1.5, -1.5, 0.0], [2.3333, 2.3333, 2.3333, 2.3333]]),
        np.array([[3.525, 5.45], [2.95, 0.4]]),
    ]

    @pytest.mark.parametrize(
        "padded_array, expected_means", zip(padded_arrays, expected_mean_sets)
    )
    def test_padded_mean_gives_mean_of_each_array(self, padded_array, expected_means):
        means = padded_mean(padded_array)

        assert tutils.npclose(means, expected_means)
