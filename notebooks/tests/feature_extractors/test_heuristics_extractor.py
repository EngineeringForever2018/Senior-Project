from notebooks.feature_extractors import HeuristicsExtractor
from numpy import ndarray


class TestHeuristicsExtractor:
    def test_heuristics_extractor_is_feature_extractor(self):
        heuristics_extractor = HeuristicsExtractor()

        features = heuristics_extractor(
            [
                "hello from the other side.",
                "i wish i could say that i tried...",
                "to tell you",
            ]
        )

        assert isinstance(features, ndarray)
        assert features.dtype == float
        assert features.ndim == 2
