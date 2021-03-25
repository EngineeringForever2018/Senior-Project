from notebooks.structures import PaddedArray

from abc import ABC, abstractmethod
from numpy import ndarray


# Note: Profile implementations currently do not have to handle empty input edge cases
#       because PaddedArray does not allow them.
# TODO: Docstrings for each of the public functions.
class BaseProfile(ABC):
    @abstractmethod
    def _feed(self, author_texts: PaddedArray):
        pass

    def feed(self, author_texts):
        author_texts, _ = self._pad_texts(author_texts)

        self._feed(author_texts)

    @abstractmethod
    def _reset(self):
        pass

    def reset(self):
        self._reset()

    @abstractmethod
    def _distances(self, suspect_texts: PaddedArray) -> ndarray:
        pass

    @abstractmethod
    def _ready(self) -> bool:
        pass

    def distances(self, suspect_texts):
        assert self._ready(), "you must feed profile before calling distances"

        suspect_texts, single = self._pad_texts(suspect_texts)

        distances_ = self._distances(suspect_texts)

        if single:
            return distances_[0]

        return distances_

    def _pad_texts(self, texts) -> PaddedArray:
        """Pad texts and also return True if input was single text"""
        if isinstance(texts, PaddedArray):
            return texts, False

        # TODO: Input checking to ensure that data is either 2-D or 3-D
        if texts.ndim == 2:
            # The general distances function will still work if we just treat the input
            # as a set of 1 text.
            return PaddedArray(texts[None, ...]), True

        return PaddedArray(texts), False
