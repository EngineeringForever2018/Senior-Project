import pickle
from io import BytesIO
import numpy as np
import pandas as pd
from notebooks.profiles import BaseProfile


class EuclideanProfile(BaseProfile):
    """
    Measures euclidean distance between the mean of the data it's fed and the mean of
    the suspect data.
    """

    def __init__(self, bytesIO = None):
        if bytesIO is not None:
            state_dict = pickle.load(bytesIO)

            if state_dict["mean"] is not None:
                mean_bytes = BytesIO(state_dict["mean"])
                mean_bytes.seek(0)
                self._mean = np.load(mean_bytes)
            else:
                self._mean = None

            self._count = state_dict["count"]
        else:
            self._mean = None
            self._count = 0

    def _feed(self, author_texts: pd.DataFrame):
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

    def _distances(self, suspect_texts: pd.DataFrame):
        """
        Get the distance from the profile to each set of observations from :param
        suspect_texts. :param suspect_texts is expected to be a (num_essays,
        num_segments, feature_dim) numpy array.
        """
        suspect_means = suspect_texts.groupby(level=-2).mean()

        suspect_diffs = self._mean - suspect_means

        return np.sqrt((suspect_diffs * suspect_diffs).sum(axis=1))

    def _author_mean(self, author_texts: pd.DataFrame):
        mean = author_texts.mean()
        count = len(author_texts)

        return mean, count

    def _reset(self):
        # WTF: This passes even though count is not reset, because the count is not
        #      considered on first feed and simply reassigned. We may want to add edge
        #      case testing here or refactor to something that doesn't contain this
        #      loophole.
        self._mean = None

    @property
    def binary(self):
        mean_bytes = BytesIO()

        if self._mean is not None:
            np.save(mean_bytes, self._mean)

            mean_bytes = mean_bytes.getvalue()
        else:
            mean_bytes = None

        state_dict = {"mean": mean_bytes, "count": self._count}

        state_bytes = BytesIO()

        pickle.dump(state_dict, state_bytes)

        state_bytes.seek(0)

        return state_bytes
