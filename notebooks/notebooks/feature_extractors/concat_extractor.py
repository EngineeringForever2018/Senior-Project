import numpy as np


class ConcatExtractor:
    def __init__(self, *args):
        self.extractors = args

    def sentence_extract(self, sentences):
        return np.concatenate([extractor.sentence_extract(sentences) for extractor in self.extractors], axis=1)
