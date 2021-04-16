from notebooks.profiles import NaiveBayesProfile
from tests import tutils
import pytest
import pandas as pd


# TODO: Triangulate and just test better in general.
class TestNaiveBayesProfile:
    author_texts = [pd.DataFrame([[2.2, 3.3, 4.4], [5.6, 7.8, 2.3], [-1.1, 1.1, 1.1]])]

    suspect_text_sets = [
        pd.DataFrame(
            [[5.4, 2.2, 8.1], [2.2, 2.2, 2.2], [3.2, 1.8, 9.9]],
            index=pd.MultiIndex.from_tuples([(0, 0), (0, 1), (0, 2)]),
        )
    ]

    expected_distance_sets = [
        pd.DataFrame(
            [-8.0926],
            index=pd.MultiIndex.from_tuples([(0,)]),
        )
    ]

    @pytest.mark.parametrize(
        "author_text, suspect_texts, expected_distances",
        zip(author_texts, suspect_text_sets, expected_distance_sets),
    )
    def test_naive_bayes_profile_should_return_normal_probabilities(
        self, author_text, suspect_texts, expected_distances
    ):
        profile = NaiveBayesProfile()

        profile.feed(author_text)
        distances = profile.distances(suspect_texts)

        assert tutils.npclose(distances, expected_distances)
