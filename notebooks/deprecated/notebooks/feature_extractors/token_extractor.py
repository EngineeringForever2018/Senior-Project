from abc import ABC, abstractmethod
from typing import List

import numpy as np
from numpy import ndarray
from tqdm import tqdm


class BaseTokenExtractor(ABC):
    @abstractmethod
    def _extract_tokens(self, tokens: List) -> ndarray:
        pass

    def __call__(self, token_matrix: List[List], show_loading=False):
        if show_loading:
            token_iter = tqdm(token_matrix)
        else:
            token_iter = token_matrix

        token_arrays = [
            self._extract_tokens(token_list)[None, ...] for token_list in token_iter
        ]

        return np.concatenate(token_arrays, axis=0)
