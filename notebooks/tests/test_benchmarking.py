from notebooks import benchmarking as bench
import numpy as np
import pytest


guess_sets = [
    np.array([True, False, True, True]),
    np.array([2, 3, 4, 1]),
    np.array([True, True, True, True, True]),
]

correct_label_sets = [
    np.array([True, True, False, False]),
    np.array([1, 3, 4, 1]),
    np.array([False, False, True, True, True]),
]

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


class TestAccuracy:
    expected_accuracies = [0.25, 0.75]

    @pytest.mark.parametrize(
        "guesses, correct_labels, expected_accuracy", zip(*inputs, expected_accuracies)
    )
    def test_accuracy_should_return_accuracy_of_guesses(
        self, guesses, correct_labels, expected_accuracy
    ):
        accuracy = bench.accuracy(guesses, correct_labels)

        assert accuracy == expected_accuracy


class TestBalancedAccuracy:
    expected_accuracies = [0.25, 0.5]

    balanced_inputs = [guess_sets[0], guess_sets[2]], [
        correct_label_sets[0],
        correct_label_sets[2],
    ]

    @pytest.mark.parametrize(
        "guesses, labels, expected_accuracy", zip(*balanced_inputs, expected_accuracies)
    )
    def test_balanced_accuracy_should_return_balanced_accuracy_of_guesses(
        self, guesses, labels, expected_accuracy
    ):
        accuracy = bench.balanced_accuracy(guesses, labels)

        assert accuracy == expected_accuracy
