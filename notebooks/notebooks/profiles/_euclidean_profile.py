import numpy as np
from notebooks.profiles import BaseProfile
from notebooks.structures import PaddedArray, padded_mean


class EuclideanProfile(BaseProfile):
    """
    Measures euclidean distance between the mean of the data it's fed and the mean of
    the suspect data.
    """

    def __init__(self):
        self._mean = None
        self._count = 0

    def _feed(self, author_texts: PaddedArray):
        """
        Feed :param author_texts into the profile, which will be compared to the suspect
        data later.
        """
        if self._mean is not None:
            # We can add to the old mean by doing a weighted average between the old
            # mean and the new mean.
            next_mean, next_count = self._author_mean(author_texts)

            new_count = self._count + next_count

            old_weight = self._count / new_count
            next_weight = next_count / new_count

            self._mean = old_weight * self._mean + next_weight * next_mean
            self.count = new_count
        else:
            self._mean, self._count = self._author_mean(author_texts)

    def _ready(self):
        return self._mean is not None

    def _distances(self, suspect_texts):
        """
        Get the distance from the profile to each set of observations from :param
        suspect_texts. :param suspect_texts is expected to be a (num_essays,
        num_segments, feature_dim) numpy array.
        """
        suspect_means = padded_mean(suspect_texts)

        suspect_diffs = self._mean - suspect_means

        return np.linalg.norm(suspect_diffs, axis=1)

    def _author_mean(self, author_texts: PaddedArray):
        text_means = padded_mean(author_texts)

        count = np.sum(author_texts.lengths)
        weights = author_texts.lengths / count

        # We must do weighted average since the different texts can have different
        # lengths.
        mean = np.sum(text_means * weights[..., None], axis=0)

        return mean, count

    def _reset(self):
        # WTF: This passes even though count is not reset, because the count is not
        #      considered on first feed and simply reassigned. We may want to add edge
        #      case testing here or refactor to something that doesn't contain this
        #      loophole.
        self._mean = None
