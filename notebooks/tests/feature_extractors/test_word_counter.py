from notebooks.feature_extractors import WordCounter
from tests import tutils
import numpy as np


class TestWordCounter:
    def test_word_counter_should_correctly_count_words(self):
        word_counter = WordCounter()

        features = word_counter(
            [
                "A sentence with five words.",
                "sunflowers in the afternoon",
                "bla , bla bla,",
                "",
            ]
        )

        assert tutils.npequal(features, np.array([[5.0], [4.0], [4.0], [0.0]]))
        assert features.dtype == float
