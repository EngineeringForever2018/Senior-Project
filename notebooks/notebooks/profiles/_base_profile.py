from notebooks.structures import PaddedArray

from abc import ABC, abstractmethod
from numpy import ndarray
import pandas as pd
import numpy as np


# Note: Profile implementations currently do not have to handle empty input edge cases
#       because PaddedArray does not allow them.
# TODO: Docstrings for each of the public functions.
class BaseProfile(ABC):
    @abstractmethod
    def _feed(self, author_texts: PaddedArray):
        pass

    def feed(self, author_texts):
        author_texts, _, _ = self._pad_texts(author_texts)

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

        suspect_texts, single, is_numpy = self._pad_texts(suspect_texts)

        distances_ = self._distances(suspect_texts)

        if single:
            return distances_[0]

        if is_numpy:
            return distances_.to_numpy()

        return distances_

    def _pad_texts(self, texts) -> pd.DataFrame:
        """Pad texts and also return True if input was single text"""
        if isinstance(texts, pd.DataFrame):
            return texts, False, False

        if isinstance(texts, PaddedArray):
            texts = [array[:length] for array, length in zip(texts.data, texts.lengths)]

            level0, level1 = zip(
                *[
                    ([index] * len(array), np.arange(len(array)))
                    for index, array in enumerate(texts)
                ]
            )
            level0, level1 = sum(level0, []), np.concatenate(level1)

            return (
                pd.DataFrame(
                    np.concatenate(texts),
                    index=pd.MultiIndex.from_tuples(zip(level0, level1)),
                ),
                False,
                True,
            )

        # TODO: Input checking to ensure that data is either 2-D or 3-D
        if texts.ndim == 2:
            # The general distances function will still work if we just treat the input
            # as a set of 1 text.
            indices = zip([0] * len(texts), np.arange(len(texts)))
            return (
                pd.DataFrame(texts, index=pd.MultiIndex.from_tuples(indices)),
                True,
                False,
            )

        level0, level1 = zip(
            *[
                ([index] * len(array), np.arange(len(array)))
                for index, array in enumerate(texts)
            ]
        )
        level0, level1 = sum(level0, []), np.concatenate(level1)

        return (
            pd.DataFrame(
                np.concatenate(texts),
                index=pd.MultiIndex.from_tuples(zip(level0, level1)),
            ),
            False,
            True,
        )
