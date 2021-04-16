# This was needed because tensorflow logs would appear whenever the classes here would
# be imported, and the only fix was changing an environment variable. But this would
# put code above import statements which PEP 8 does not like, and its annoying to have
# to write noqa after every import statement.

from pathlib import Path

import os
import numpy as np
from notebooks.feature_extractors import FeatureConcatenator, CommaCounter, WordCounter
from notebooks.profiles import EuclideanProfile
from numpy import ndarray
from io import BytesIO
from notebooks.segmenters import Sentencizer


class PreprocessedText:
    def __init__(self, data: ndarray):
        if isinstance(data, BytesIO):
            self._data = np.load(data)
        else:
            self._data = data

    @property
    def data(self) -> ndarray:
        return self._data

    @property
    def binary(self) -> BytesIO:
        bytesIO = BytesIO()

        np.save(bytesIO, self._data)
        bytesIO.seek(0)

        return bytesIO


class StyleProfile:
    def __init__(self, bytesIO: BytesIO = None):
        if bytesIO is not None:
            self._profile = EuclideanProfile(bytesIO)
        else:
            self._profile = EuclideanProfile()
        # TODO: Find good threshold
        self._threshold = 1.0

    def feed(self, text: PreprocessedText):
        self._profile.feed(text.data)

    def flag(self, text: PreprocessedText) -> bool:
        distance = self._profile.distances(text.data)
        return distance > self._threshold

    @property
    def binary(self):
        return self._profile.binary


class TextProcessor:
    def __init__(self):
        # TODO: Write segmenters
        self._segmenter = Sentencizer()
        self._feature_extractor = FeatureConcatenator(CommaCounter(), WordCounter())

    def __call__(self, text: str) -> PreprocessedText:
        segments = self._segmenter(text)
        return PreprocessedText(self._feature_extractor(segments))
