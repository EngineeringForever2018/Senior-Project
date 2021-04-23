from notebooks.profiles import BaseProfile
import numpy as np
import pandas as pd
import math
from io import BytesIO
import pickle


class VotingProfile(BaseProfile):
    def __init__(self, p=None, bytesIO=None):
        if bytesIO is not None:
            state_dict = pickle.load(bytesIO)

            if state_dict["mean"] is not None:
                mean_bytes = BytesIO(state_dict["mean"])
                sentences_bytes = BytesIO(state_dict["sentences"])
                mean_bytes.seek(0)
                sentences_bytes.seek(0)
                self._mean = np.load(mean_bytes)
                self._author_sentences = np.load(sentences_bytes)
                self._threshold = state_dict["threshold"]
                self._p = state_dict["p"]
            else:
                self._p = p
                self._mean = None
                self._threshold = None
                self._author_sentences = None
        else:
            self._p = p
            self._mean = None
            self._threshold = None
            self._author_sentences = None

    def _feed(self, author_texts):
        if self._author_sentences is not None:
            self._author_sentences = np.concatenate([self._author_sentences, author_texts.to_numpy()])
        else:
            self._author_sentences = author_texts.to_numpy()

        excluded_distances = self._excluded_distances(self._author_sentences)

        sorted_distances = np.sort(excluded_distances)

        self._threshold = sorted_distances[math.floor(len(sorted_distances) * self._p)]

        self._mean = np.mean(self._author_sentences)
    
    def _distances(self, suspect_texts):
        flags = self.sentence_flags(suspect_texts)

        return flags.groupby(level=-2).mean()

    def sentence_flags(self, suspect_texts):
        if isinstance(suspect_texts, np.ndarray):
            suspect_texts = pd.DataFrame(suspect_texts)

        diffs = self._mean - suspect_texts

        distances = pd.DataFrame(np.linalg.norm(diffs, axis=1), index=diffs.index)

        return distances > self._threshold

    def _ready(self):
        return self._author_sentences is not None

    def _reset(self):
        self._author_sentences = None
        self._threshold = None
        self._mean = None

    def _excluded_distances(self, matrix):
        count = len(matrix)
        result = np.zeros(shape=[count])

        for i in range(count):
            other_sentences = np.delete(matrix, i, axis=0)
            other_mean = np.mean(other_sentences, axis=0)

            result[i] = np.linalg.norm(matrix[i] - other_mean)

        return result

    @property
    def binary(self):
        mean_bytes = BytesIO()
        sentences_bytes = BytesIO()

        if self._mean is not None:
            np.save(mean_bytes, self._mean)
            np.save(sentences_bytes, self._author_sentences)

            mean_bytes = mean_bytes.getvalue()
            sentences_bytes = sentences_bytes.getvalue()
        else:
            mean_bytes = None
            sentences_bytes = None

        state_dict = {"mean": mean_bytes, "sentences": sentences_bytes, "threshold": self._threshold, "p": self._p}

        state_bytes = BytesIO()

        pickle.dump(state_dict, state_bytes)

        state_bytes.seek(0)

        return state_bytes
