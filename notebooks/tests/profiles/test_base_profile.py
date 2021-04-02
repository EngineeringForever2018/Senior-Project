from notebooks.profiles import EuclideanProfile
import numpy as np
import pytest
from tests import tutils


# TODO: Error handling whenever distances are asked for without feeding.
# TODO: Batch profile generation (Maybe)
# TODO: Refactor profiles and feature extractors to only accept DataFrames and only
#       return DataFrames. (Maybe use inherited version of DataFrame).
class TestBaseProfile:
    profiles = [EuclideanProfile(), EuclideanProfile(), EuclideanProfile()]

    author_texts = [
        np.array([[-5.3, -4.1, -2.2, -1.3], [1.4, -3.2, -2.1, 0.5]]),
        np.array([[[0.1, -0.1], [-5.4, 9.2]], [[-4.8, -4.4], [7.7, 2.3]]]),
        np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0], [-1.0, 4.0, -5.0]]),
    ]

    suspect_texts = [
        np.array([[1.0, 2.0, 3.0, 4.0], [4.0, 3.0, 2.0, 1.0], [3.5, 3.5, 3.5, 3.5]]),
        np.array(
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[5.5, 7.5], [-8.6, 6.8]],
                [[-3.2, 4.3], [2.2, 1.2]],
            ]
        ),
        np.array(
            [
                [[1.5, 2.5, 3.5], [0.5, 0.5, 0.5], [-1.5, -4.5, -5.5]],
                [[10.0, 9.5, 5.0], [-4.4, 8.0, 7.0], [6.7, 7.8, -13.0]],
            ]
        ),
    ]

    expected_distances = [
        10.0101,
        np.array([1.6651, 5.4829, 1.0050]),
        np.array([2.5111, 7.6360]),
    ]

    @pytest.mark.parametrize(
        "profile, author_text, suspect_text, expected_distance",
        zip(profiles, author_texts, suspect_texts, expected_distances),
    )
    def test_profile_should_work_for_single_observation(
        self, profile, author_text, suspect_text, expected_distance
    ):
        profile.feed(author_text)
        distance = profile.distances(suspect_text)

        assert tutils.npclose(distance, expected_distance)

    @pytest.mark.parametrize("suspect_text", suspect_texts)
    def test_profile_should_not_score_when_unfed(self, suspect_text):
        profile = EuclideanProfile()
        with pytest.raises(AssertionError):
            _ = profile.distances(suspect_text)
