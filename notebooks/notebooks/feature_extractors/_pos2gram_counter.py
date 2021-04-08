from typing import List

import numpy as np
from numpy import ndarray
from pkg_resources import resource_stream
from notebooks import utils

from notebooks.feature_extractors import BaseSegmentExtractor

posVector = [
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SPACE",
    "SYM",
    "VERB",
    "X",
]

Phi_size = len(posVector) * len(posVector)

# TODO: Tests
class POS2GramCounter(BaseSegmentExtractor):
    def __init__(self, best=30):
        self.sorted_indices = np.load(
            resource_stream("notebooks.resources", "best_bigrams.npy")
        )[:best]
        self._nlp = utils.default_nlp()

    def _segment_extract(self, segment):
        posArr = [token.pos_ for token in self._nlp(segment)]

        Phi = np.zeros(Phi_size)

        k = 0

        for i in range(len(posArr) - 1):
            if i == 0:
                l = posVector.index(str(posArr[i]))
                k = posVector.index(str(posArr[i + 1]))
                Phi[l * len(posVector) + k] += 1
            else:
                l = posVector.index(str(posArr[i + 1]))
                Phi[k * len(posVector) + l] += 1
                k = l
        return Phi
