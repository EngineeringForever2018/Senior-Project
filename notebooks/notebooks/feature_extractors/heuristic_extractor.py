import numpy as np
from numpy import ndarray

from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor
from notebooks.feature_extractors.parsed_doc import ParsedDoc
from notebooks.utils import split_text


class HeuristicExtractor(BaseFeatureExtractor):
    def __init__(self, paragraph_length):
        self.paragraph_length = paragraph_length

    def extract(self, text: str) -> ndarray:
        paragraphs = split_text(text, sentences_per_split=self.paragraph_length)

        parsed_docs = [ParsedDoc(paragraph) for paragraph in paragraphs]
        parsed_matrix_list = [[parsed_doc.getWordCount(), parsed_doc.getCommaCount(),
                               parsed_doc.getPeriodCount(), parsed_doc.getPToWRatio()] for parsed_doc in parsed_docs]

        return np.array(parsed_matrix_list)