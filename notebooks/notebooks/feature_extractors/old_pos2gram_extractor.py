from numpy import ndarray

from notebooks.feature_extractors.old_pos2gram_token_extractor import OldPOS2GramTokenExtractor
from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor
# TODO: Refactor this into a POSNGramExtractor that takes n as a constructor parameter
from notebooks.segmentation import POSSentenceTokenizer


class OldPOS2GramExtractor(BaseFeatureExtractor):
    def __init__(self, paragraph_length, best=30):
        self.tokenizer = POSSentenceTokenizer()
        self.token_extractor = OldPOS2GramTokenExtractor(best=best)

    def extract(self, text: str) -> ndarray:
        token_matrix = self.tokenizer.tokenize(text)

        return self.token_extractor(token_matrix)

    def sentence_extract(self, sentences):
        token_matrix = self.tokenizer.tokenize_list(sentences)

        return self.token_extractor(token_matrix)
