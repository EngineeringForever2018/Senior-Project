import numpy as np
from scipy import stats
from scipy.spatial.distance import mahalanobis


class MahalanobisProfile:
    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor
        self._v = None
        self._u = None

    def feed(self, text: str):
        features = self.feature_extractor(text)

        features = features.T

        self._v = np.cov(features)
        self._u = np.reshape(np.mean(features, axis=1), [-1])

    def score(self, text: str):
        features = self.feature_extractor(text)

        feature = features[np.random.randint(0, len(features))]

        inv = np.linalg.inv(self._v)
        distance = np.matmul(np.matmul((self._u - feature), inv), (self._u - feature).T)
        # distance = mahalanobis(self._u, feature, np.linalg.inv(self._v))
        # distance = distance**2

        n = len(feature)

        return 1. - stats.chi2.cdf(distance, n)

