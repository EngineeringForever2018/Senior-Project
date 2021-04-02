from notebooks.feature_extractors import CommaCounter
import pytest
from tests import tutils
import numpy as np
import pandas as pd


# TODO: Edge cases
# TODO: Word length feature extractor
# TODO: Thresholder
# TODO: Benchmark code
class TestCommaCounter:
    segment_sets = [
        ["This has no commas.", "This has 1, comma.", "This has, 2, commas."],
        ["a sentence with one, comma", "another se,n,,t,, with not telling..."],
        pd.DataFrame(
            ["a , ,", ", , , ,,", ",,,"],
            columns=["text"],
            index=pd.MultiIndex.from_tuples([(0, 0), (1, 0), (1, 1)]),
        ),
    ]

    expected_feature_sets = [
        np.array([[0.0], [1.0], [2.0]]),
        np.array([[1.0], [5.0]]),
        pd.DataFrame(
            [[2.0], [5.0], [3.0]],
            index=pd.MultiIndex.from_tuples([(0, 0), (1, 0), (1, 1)]),
        ),
    ]

    @pytest.mark.parametrize(
        "segments, expected_features", zip(segment_sets, expected_feature_sets)
    )
    def test_comma_counter_should_count_commas(self, segments, expected_features):
        comma_counter = CommaCounter()

        features = comma_counter(segments)

        assert tutils.npequal(features, expected_features)
        if not isinstance(features, pd.DataFrame):
            assert features.dtype == float
