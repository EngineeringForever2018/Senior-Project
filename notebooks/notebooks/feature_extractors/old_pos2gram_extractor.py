import numpy as np
from numpy import ndarray

from notebooks.feature_extractors import pospca_helpers as avpd
from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor


# TODO: Refactor this into a POSNGramExtractor that takes n as a constructor parameter
from notebooks.utils import split_text


class OldPOS2GramExtractor(BaseFeatureExtractor):
    def __init__(self, paragraph_length):
        self.paragraph_length = paragraph_length

    def extract(self, text: str) -> ndarray:
        paragraphs = split_text(text, sentences_per_split=self.paragraph_length)

        # Add Phi samples (x-xBar) to Phi, stored as a list for ease of use but imagine its a 2D array stored vertically
        X_list = []
        for paragraph in paragraphs:
            X_list.append(avpd.make_X(paragraph)[None, ...])

        return np.concatenate(X_list)

    @staticmethod
    def sentence_extract(sentences):
        X_list = []
        for sentence in sentences:
            X_list.append(avpd.make_X(sentence)[None, ...])

        return np.concatenate(X_list)
