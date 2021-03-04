from spacy.lang.en import English

from notebooks.feature_extractors import POSPCAExtractor
from notebooks.utils import split_into_sentences


class TestExtractors:
    def test_1000_sentences_split_fast(self, benchmark):
        text = 'This is a sentence. ' * 1000
        nlp_fast = English()
        nlp_fast.add_pipe('sentencizer')

        def split_sentences():
            return list(split_into_sentences(text, nlp=nlp_fast))

        benchmark(split_sentences)

    def test_1000_sentences_split(self, benchmark):
        text = 'This is a sentence. ' * 1000

        def split_sentences():
            return list(split_into_sentences(text))

        benchmark(split_sentences)

    def test_1000_sentences(self, benchmark):
        text = 'This is a sentence. ' * 1000
        extractor = POSPCAExtractor(paragraph_length=4, n_components=10)

        benchmark(extractor, text)
