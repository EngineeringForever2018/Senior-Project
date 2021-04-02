import numpy as np
import pandas as pd

from notebooks.profiles import EuclideanProfile
from notebooks.structures import PaddedArray
from tests import tutils
import pytest


class TestEuclideanProfile:
    author_texts = [
        PaddedArray(
            [
                np.array([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0]]),
                np.array([[4.2, -5.5, 2.1], [3.3, 3.4, 3.2], [-1.2, -2.2, -3.2]]),
            ]
        ),
        pd.DataFrame(
            [[2.5, -3.3], [2.3, 2.3], [1.1, 2.1], [-2.0, -5.5], [8.3, 9.2]],
            columns=["random", "column"],
            index=pd.MultiIndex.from_tuples(
                [(5, 0), (5, 1), (5, 2), (8, 0), (8, 1)], names=["name0", "name69"]
            ),
        ),
    ]

    suspect_text_sets = [
        PaddedArray(
            [
                np.array([[2.2, 3.3, 4.4], [0.4, 9.0, 0.2], [5.3, 3.2, 19.8]]),
                np.array([[-2.4, -1.2, -3.3], [-1.3, -12.2, -3.2]]),
            ]
        ),
        pd.DataFrame(
            [[2.9, -3.3], [1.1, 2.1], [-2.0, -5.5], [8.3, 9.2]],
            columns=["random", "column"],
            index=pd.MultiIndex.from_tuples(
                [(9, 0), (3, 0), (3, 1), (3, 2)], names=["name0", "name69"]
            ),
        ),
    ]

    expected_distance_sets = [
        np.array([9.4597, 8.0542]),
        pd.Series(
            [0.9737, 4.2848],
            index=pd.MultiIndex.from_tuples([(3,), (9,)], names=["name0"]),
        ),
    ]

    @pytest.mark.parametrize(
        "author_text, suspect_texts, expected_distances",
        zip(author_texts, suspect_text_sets, expected_distance_sets),
    )
    def test_euclidean_profile_should_compare_means(
        self, author_text, suspect_texts, expected_distances
    ):
        profile = EuclideanProfile()

        profile.feed(author_text)
        distances = profile.distances(suspect_texts)

        assert tutils.npclose(distances, expected_distances)


class TestMultipleFeeds:
    author_text_sets = [
        [
            PaddedArray([np.array([[2.0, 2.0, 3.0, 2.0], [1.0, 0.0, 1.5, -6.0]])]),
            PaddedArray(
                [
                    np.array(
                        [
                            [4.0, -16.5, 4.3, 7.7],
                            [1.1, -20.3, 10.9, 8.8],
                            [3.3, 5.2, 3.4, 0.2],
                        ]
                    ),
                    np.array([[1.2, 3.3, 3.3, 4.4]]),
                ]
            ),
        ],
        [PaddedArray([np.array([[2.0, 2.0, 3.0, 2.0], [1.0, 0.0, 1.5, -6.0]])])] * 3,
    ]

    suspect_text_sets = [
        PaddedArray([np.array([[4.4, 4.4, 4.4, 4.4], [8.8, 8.8, 8.8, 8.8]])]),
        PaddedArray(
            [
                np.array(
                    [[3.3, 3.3, 3.3, 3.3], [2.2, 2.2, 2.2, 2.2], [1.1, 1.1, 1.1, 1.1]]
                ),
                np.array([[4.4, 4.4, 4.4, 4.4], [2.2, 2.2, 2.2, 2.2]]),
            ]
        ),
    ]

    expected_distance_sets = [np.array([12.6407]), np.array([4.4241, 6.1419])]

    @pytest.mark.parametrize(
        "author_texts, suspect_texts, expected_distances",
        zip(author_text_sets, suspect_text_sets, expected_distance_sets),
    )
    def test_profile_should_accumulate_feeds(
        self, author_texts, suspect_texts, expected_distances
    ):
        profile = EuclideanProfile()

        for author_text in author_texts:
            profile.feed(author_text)
        distances = profile.distances(suspect_texts)

        assert tutils.npclose(distances, expected_distances)

    @pytest.mark.parametrize(
        "author_texts, suspect_texts", zip(author_text_sets, suspect_text_sets)
    )
    def test_profile_should_allow_resets(self, author_texts, suspect_texts):
        profile = EuclideanProfile()

        profile.feed(author_texts[0])
        expected_distances = profile.distances(suspect_texts)

        for author_text in author_texts:
            profile.feed(author_text)
        profile.reset()
        profile.feed(author_texts[0])
        distances = profile.distances(suspect_texts)

        assert tutils.npclose(distances, expected_distances)
