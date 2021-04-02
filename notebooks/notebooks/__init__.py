# from notebooks.profiles.style_profile import StyleProfile
from pathlib import Path
from notebooks.feature_extractors import FeatureConcatenator, CommaCounter, WordCounter
from notebooks.profiles import EuclideanProfile


class PreprocessedText:
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def file(self, file_path: str):
        return open(Path(file_path), "w")


class StyleProfile:
    def __init__(self):
        self._profile = EuclideanProfile()
        # TODO: Find good threshold
        self._threshold = 1.0

    def feed(self, text: PreprocessedText):
        self._profile.feed(text.data())

    def flag(self, text: PreprocessedText) -> bool:
        distance = self._profile.distances(text.data)
        return distance > self._threshold

    def file(self, file_path: str):
        return open(Path(file_path), "w")


class TextProcessor:
    def __init__(self):
        # TODO: Write segmenters
        self._segmenter = None
        self._feature_extractor = FeatureConcatenator(CommaCounter(), WordCounter())

    def __call__(self, text: str) -> PreprocessedText:
        segments = self._segmenter(text)
        return PreprocessedText(self._feature_extractor(segments))


# TODO: Driver
