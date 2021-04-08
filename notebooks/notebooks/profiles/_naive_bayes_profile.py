from notebooks.profiles import BaseProfile
import numpy as np
from scipy.stats import norm


# Note: Classes like this aren't going to completely follow Bayes rule or perfectly
#       calculate the normal PDF, because they don't have to. They just have to
#       calculate something proportional so that a good threshold can be found.
class NaiveBayesProfile(BaseProfile):
    def __init__(self):
        self._author_mean = None
        self._author_std = None

    def _feed(self, author_texts):
        self._author_mean = author_texts.mean()
        self._author_std = author_texts.std()

    def _distances(self, suspect_texts):
        z_scores = (suspect_texts - self._author_mean) / self._author_std

        densities = z_scores.copy()
        densities[:] = norm.pdf(densities[:])

        log_densities = np.log(densities)
        
        segment_distances = log_densities.sum(axis=1)

        group_distances = segment_distances.groupby(level=-2).mean()

        return group_distances

    def _ready(self):
        return self._author_mean is not None

    def _reset(self):
        self._author_mean = None
        self._author_std = None
