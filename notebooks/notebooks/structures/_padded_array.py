import numpy as np
from numpy import ndarray
from typing import List


# Note: In the future padded array operations can be optimized, because they can treat
#       the data as not padded if necessary. A boolean attribute telling whether the
#       data is actually padded would accomplish this.
# Note: We technically shouldn't expose data because it makes too many promises about
#       internal data. However, making it private would cost a lot of convenience and
#       I don't currently see it being a problem.
class PaddedArray:
    """
    Pads arrays with zeroes so that they are all of shape (max_length, feature_dim).
    """

    # TODO: Decide during benchmarking if this needs optimizing and if so optimize for
    #       special cases.
    def __init__(self, arrays: List[ndarray]):
        """
        :param arrays: A list of numpy arrays to pad.
        """
        if len(arrays) == 0:
            raise EmptyListException("arrays parameter must not be empty")

        for array in arrays:
            if array.size == 0:
                raise EmptyArrayException("Found an empty array")

        lengths = [array.shape[0] for array in arrays]

        # Arrays should be padded to max length by feature dimension
        max_length = max(lengths)
        # TODO: This line may need to change if emtpy arrays are supported
        feature_dim = arrays[0].shape[1]

        # We pad with zeros, not supporting any other type of padding
        data = np.zeros([len(arrays), max_length, feature_dim])

        for index, (array, length) in enumerate(zip(arrays, lengths)):
            data[index, 0:length] = array

        self._data = data
        self._lengths = np.array(lengths)

    @property
    def data(self) -> ndarray:
        """The padded data."""
        return self._data

    @property
    def lengths(self) -> ndarray:
        """The lengths of each array"""
        return self._lengths


def padded_mean(padded_array: PaddedArray):
    """Give the mean of the :param padded_array along axis 1"""
    # Lengths are reshaped so that they align with the first dimension
    return np.sum(padded_array.data, axis=1) / padded_array.lengths[..., None]


class EmptyListException(Exception):
    pass


class EmptyArrayException(Exception):
    pass
