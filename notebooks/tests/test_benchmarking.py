from notebooks import benchmarking as bench
import numpy as np
import pytest


guess_sets = [np.array([True, False, True, True]), np.array([2, 3, 4, 1])]

correct_label_sets = [np.array([True, True, False, False]), np.array([1, 3, 4, 1])]

inputs = (guess_sets, correct_label_sets)


class TestCorrectCount:
    expected_correct_counts = [1, 3]

    @pytest.mark.parametrize(
        "guesses, correct_labels, expected_correct_count",
        zip(*inputs, expected_correct_counts),
    )
    def test_correct_count_should_return_number_of_correct_guesses(
        self, guesses, correct_labels, expected_correct_count
    ):
        correct_count = bench.correct_count(guesses, correct_labels)

        assert correct_count == expected_correct_count
