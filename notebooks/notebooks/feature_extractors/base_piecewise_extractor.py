from abc import ABC, abstractmethod
from typing import List

from numpy import ndarray
import numpy as np


class BasePiecewiseExtractor(ABC):
    @abstractmethod
    def _extract_piece(self, piece: str) -> ndarray:
        pass

    def __call__(self, pieces: List[str]) -> ndarray:
        piece_arrays = [self._extract_piece(piece)[None, ...]
                        for piece in pieces]

        return np.concatenate(piece_arrays, axis=0)
