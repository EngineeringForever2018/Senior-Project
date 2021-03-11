from typing import List

import numpy as np
from numpy import ndarray

from notebooks.feature_extractors import pospca_helpers as avpd
from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor


# TODO: Refactor this into a POSNGramExtractor that takes n as a constructor parameter
from notebooks.feature_extractors.token_extractor import BaseTokenExtractor
from notebooks.utils import split_text


class OldPOS2GramTokenExtractor(BaseTokenExtractor):
    def __init__(self):
        pass

    def _extract_tokens(self, tokens: List) -> ndarray:
        return avpd.make_X(tokens)
