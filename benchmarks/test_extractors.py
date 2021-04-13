from spacy.lang.en import English

from notebooks.feature_extractors.old_pos2gram_token_extractor import OldPOS2GramTokenExtractor
from notebooks.feature_extractors.posngram_token_extractor import POSNGramTokenExtractor
from notebooks.segmentation.pos_sentence_tokenizer import POSSentenceTokenizer
from notebooks.utils import split_into_sentences


class TestExtractors:
    def test_1000_sentences_split_fast(self, benchmark):
        text = 'This is a sentence. ' * 1000
        nlp_fast = English()
        nlp_fast.add_pipe('sentencizer')

        def split_sentences():
            return list(split_into_sentences(text, nlp=nlp_fast))

        benchmark(split_sentences)

    # def test_1000_sentences_split(self, benchmark):
    #     text = 'This is a sentence. ' * 1000
    #
    #     def split_sentences():
    #         return list(split_into_sentences(text))
    #
    #     benchmark(split_sentences)
    #
    # def test_1000_sentences(self, benchmark):
    #     text = 'This is a sentence. ' * 1000
    #     extractor = POSPCAExtractor(paragraph_length=4, n_components=10)
    #
    #     benchmark(extractor, text)

    text = 'My name is Sir Gregory Bourbon the third, I came to this continent so that I could secure a fine piece ' \
           'of land' * 1000
    tokenized = POSSentenceTokenizer()(text)

    def test_1000_sentences_old(self, benchmark):
        extractor = OldPOS2GramTokenExtractor()

        benchmark(extractor, self.tokenized)

    def test_1000_sentences_new(self, benchmark):
        extractor = POSNGramTokenExtractor(n=2)

        benchmark(extractor, self.tokenized)
