from notebooks.thresholders import SimpleAccuracyThresholder
import pytest
import numpy as np


# TODO: Error condition: No distances
# TODO: Error condition: Different lengths between distances and label
# TODO: Error condition: Negative distances
class TestSimpleAccuracyThresholder:
    distance_sets = [
        np.array([1.0, 2.0, 3.0, 4.0]),
        np.array([3.2, 5.8, 17.0, 200.11, 31.3, 15.2, 8.9, 49.2]),
        np.array([4.0, 3.0, 5.0, 8.0, 9.0, 2.0]),
        np.array([10.0, 11.0, 12.0, 13.0, 14.0]),
    ]

    label_sets = [
        np.array([False, False, True, True]),
        np.array([False, True, False, True, True, False, False, True]),
        np.array([True, True, False, True, True, True]),
        np.array([False, True, False, False, False]),
    ]

    expected_thresholds = [2.5, 24.15, -1.0, float("inf")]

    @pytest.mark.parametrize(
        "distances, labels, expected_threshold",
        zip(distance_sets, label_sets, expected_thresholds),
    )
    def test_simple_thresholder_should_find_best_threshold(
        self, distances, labels, expected_threshold
    ):
        thresholder = SimpleAccuracyThresholder()

        threshold = thresholder(distances, labels)

        assert threshold == expected_threshold
