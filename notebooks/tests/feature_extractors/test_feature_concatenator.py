from notebooks.feature_extractors import FeatureConcatenator, CommaCounter, WordCounter
from tests import tutils
import numpy as np


class TestFeatureConcatenator:
    def test_feature_concatenator_should_correctly_count_words(self):
        feature_concatenator = FeatureConcatenator(CommaCounter(), WordCounter())

        features = feature_concatenator(
            [
                "A sentence with some, words.",
                "sunflowers in the afternoon",
                "bla , bla bla,",
                "",
            ]
        )

        assert tutils.npequal(
            features, np.array([[1.0, 5.0], [0.0, 4.0], [2.0, 4.0], [0.0, 0.0]])
        )
        assert features.dtype == float
