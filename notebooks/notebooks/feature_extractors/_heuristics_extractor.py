from notebooks.feature_extractors import FeatureConcatenator, CommaCounter, WordCounter


class HeuristicsExtractor(FeatureConcatenator):
    def __init__(self):
        super().__init__(CommaCounter(), WordCounter())
