from typing import List, Union

import numpy as np
from scipy import stats
from scipy.spatial.distance import mahalanobis


class MahalanobisProfile:
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor
        self._v = None
        self._u = None

    def reset(self):
        self._v = None
        self._u = None

    def feed(self, text: Union[str, List[str]]):
        features = self.feature_extractor(text)

        features = features.T

        self._v = np.cov(features)
        self._u = np.reshape(np.mean(features, axis=1), [-1])

    def sentence_feed(self, sentences):
        features = self.feature_extractor.sentence_extract(sentences)

        features = features.T

        self._v = np.cov(features)
        self._u = np.reshape(np.mean(features, axis=1), [-1])

    def score(self, text: Union[str, List[str]]):
        features = self.feature_extractor(text)

        feature, distance = self.score_helper(features)

        if distance == 'RAISE':
            return 0.

        n = len(feature)

        return 1. - stats.chi2.cdf(distance, n)

    def score_helper(self, features):
        # feature = features[np.random.randint(0, len(features))]
        feature = np.mean(features, axis=0)

        try:
            inv = np.linalg.inv(self._v)
        except np.linalg.LinAlgError:
            return None, 'RAISE'
        distance = np.matmul(np.matmul((self._u - feature), inv), (self._u - feature).T)
        # distance = mahalanobis(self._u, feature, np.linalg.inv(self._v))
        # distance = distance**2

        return feature, distance

    def sentence_score(self, sentences):
        features = self.feature_extractor.sentence_extract(sentences)

        feature, distance = self.score_helper(features)

        if distance == 'RAISE':
            return 0.

        n = len(feature)

        return 1. - stats.chi2.cdf(distance, n)

