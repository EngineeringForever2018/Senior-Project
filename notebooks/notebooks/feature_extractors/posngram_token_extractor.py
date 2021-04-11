from typing import List

import numpy as np
from numpy import ndarray

# TODO: Refactor this into a POSNGramExtractor that takes n as a constructor parameter
from notebooks.feature_extractors.token_extractor import BaseTokenExtractor
from notebooks.utils import POSVocab


class POSNGramTokenExtractor(BaseTokenExtractor):
    def __init__(self, n, vocab=None):
        self.n = n
        self.vocab = vocab or POSVocab()
        self.vocab_len = len(self.vocab)

    # def extract(self, text: str) -> ndarray:
    #     paragraphs = split_text(text, sentences_per_split=self.paragraph_length)
    #
    #     # Add Phi samples (x-xBar) to Phi, stored as a list for ease of use but imagine its a
    #     2D array stored vertically
    #     X_list = []
    #     for paragraph in paragraphs:
    #         X_list.append(avpd.make_X(paragraph)[None, ...])
    #
    #     return np.concatenate(X_list)

    def _extract_tokens(self, tokens: List) -> ndarray:
        ngram_counts = np.zeros(self.vocab_len ** self.n)

        for index in range(0, len(tokens) - self.n + 1):
            indices = [index + range_index for range_index in range(0, self.n)]

            ngram_index = self._ngram_index([self.vocab[index_] for index_ in indices])

            ngram_counts[ngram_index] += 1

        return ngram_counts

    def _ngram_index(self, pos_indices):
        position_multiplier = self.vocab_len - 1

        positions = [pos_index * (position_multiplier - index) for index, pos_index in enumerate(pos_indices)]

        return sum(positions)

    # @staticmethod
    # def sentence_extract(sentences):
    #     X_list = []
    #     for sentence in sentences:
    #         X_list.append(avpd.make_X(sentence)[None, ...])
    #
    #     return np.concatenate(X_list)
