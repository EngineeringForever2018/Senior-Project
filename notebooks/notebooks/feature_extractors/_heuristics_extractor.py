from notebooks.feature_extractors import (
    FeatureConcatenator,
    CommaCounter,
    WordCounter,
    Normalizer,
    CharCounter,
    FunctionWordCounter,
)


class HeuristicsExtractor(Normalizer):
    def __init__(self):
        feature_extractor = FeatureConcatenator(CommaCounter(), CharCounter())
        count_extractor = WordCounter()
        super().__init__(feature_extractor, count_extractor)
