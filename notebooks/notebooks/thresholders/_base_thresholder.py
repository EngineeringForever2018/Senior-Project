from abc import ABC, abstractmethod
from numpy import ndarray


class BaseThresholder(ABC):
    """
    The BaseThresholder class. Thresholders should accept a set of distances and a set
    a set of labels for each distance and return a threshold to label new distances
    with.
    """

    def __call__(self, distances, labels):
        """Find a threshold for the given :param distances and :param labels."""
        return self._threshold(distances, labels)

    @abstractmethod
    def _threshold(self, distances: ndarray, labels: ndarray) -> float:
        pass
