from notebooks.feature_extractors import Normalizer, WordCounter, CharCounter
from tests import tutils
import numpy as np


# TODO: Edge case when count extractor returns 0
class TestNormalizer:
    def test_normalizer_should_normalize_features(self):
        normalizer = Normalizer(WordCounter(), CharCounter())

        features = normalizer(["hi my name is george", "GEUWV dkdk dk", "yes indeed"])

        assert tutils.npclose(features, np.array([[0.25], [0.23077], [0.2]]))
