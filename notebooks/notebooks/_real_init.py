# This was needed because tensorflow logs would appear whenever the classes here would
# be imported, and the only fix was changing an environment variable. But this would
# put code above import statements which PEP 8 does not like, and its annoying to have
# to write noqa after every import statement.

from pathlib import Path

import os
import numpy as np
from notebooks.feature_extractors import FeatureConcatenator, CommaCounter, WordCounter
from notebooks.profiles import EuclideanProfile, VotingProfile
from numpy import ndarray
from io import BytesIO
from notebooks.segmenters import Sentencizer
import pickle


class PreprocessedText:
    def __init__(self, data: ndarray, sentences=None):
        if isinstance(data, BytesIO):
            state_dict = pickle.load(data)

            data_bytes = BytesIO(state_dict["data"])
            data_bytes.seek(0)
            self._data = np.load(data_bytes)

            self._sentences = state_dict["sentences"]
        else:
            self._data = data
            self._sentences = sentences

    @property
    def data(self) -> ndarray:
        return self._data

    @property
    def sentences(self):
        return self._sentences

    @property
    def binary(self) -> BytesIO:
        data_bytes = BytesIO()

        np.save(data_bytes, self._data)
        data_bytes = data_bytes.getvalue()

        state_dict = {"data": data_bytes, "sentences": self._sentences}

        state_bytes = BytesIO()

        pickle.dump(state_dict, state_bytes)

        state_bytes.seek(0)

        return state_bytes


class StyleProfile:
    def __init__(self, bytesIO: BytesIO = None):
        if bytesIO is not None:
            self._profile = VotingProfile(p=0.7, bytesIO=bytesIO)
        else:
            self._profile = VotingProfile(p=0.7)
        self._threshold = 0.5

    def feed(self, text: PreprocessedText):
        self._profile.feed(text.data)

    def flag(self, text: PreprocessedText) -> bool:
        distance = self._profile.distances(text.data)
        return distance > self._threshold

    def detailed(self, text: PreprocessedText):
        flags = self._profile.sentence_flags(text.data)[0].tolist()

        return flags, text.sentences

    @property
    def binary(self):
        return self._profile.binary


class TextProcessor:
    def __init__(self):
        self._segmenter = Sentencizer()
        self._feature_extractor = FeatureConcatenator(CommaCounter(), WordCounter())

    def __call__(self, text: str) -> PreprocessedText:
        segments = self._segmenter(text)
        return PreprocessedText(self._feature_extractor(segments), segments)
