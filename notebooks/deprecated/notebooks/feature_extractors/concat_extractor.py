import numpy as np

from notebooks.utils import split_into_sentences


class ConcatExtractor:
    def __init__(self, *args):
        self.extractors = args

    def sentence_extract(self, sentences):
        return np.concatenate(
            [extractor.sentence_extract(sentences) for extractor in self.extractors],
            axis=1,
        )

    def __call__(self, text):
        sentences = list(split_into_sentences(text))

        return self.sentence_extract(sentences)
