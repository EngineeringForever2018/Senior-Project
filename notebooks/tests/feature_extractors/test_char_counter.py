from notebooks.feature_extractors import CharCounter
from tests import tutils
import numpy as np


class TestCharCounter:
    def test_char_counter_should_return_number_of_chars_in_string(self):
        char_counter = CharCounter()

        char_counts = char_counter(["hello, ", "", "et tu?", "   "])

        assert tutils.npequal(char_counts, np.array([[7.0], [0.0], [6.0], [3.0]]))
        assert char_counts.dtype == float
