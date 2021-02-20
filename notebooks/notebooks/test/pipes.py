from unittest.mock import MagicMock

import pandas as pd
import pytest

from notebooks import pipes


# Mocks
def mock_nlp_call(text):
    mock_sentences = [MagicMock(), MagicMock()]
    mock_sentences[0].text = 'I am sentence 1.'
    mock_sentences[1].text = 'I am sentence 2.'

    result = MagicMock()
    result.sents = (mock_sentence for mock_sentence in mock_sentences)  # noqa

    return result


# Should act like a spacy NLP object
mock_nlp = MagicMock(side_effect=mock_nlp_call)


class TestSplitText:
    dataframes = [
        pd.DataFrame([
            [5, 'I am example text', 'blueberry'],
            [7, 'I am another example text', 'cherry']
        ], columns=['author', 'text', 'flavor'])
    ]

    expected_dataframes = [
        pd.DataFrame([
            [5, 0, 0, 'I am sentence 1.', 'blueberry'],
            [5, 0, 1, 'I am sentence 2.', 'blueberry'],
            [7, 1, 0, 'I am sentence 1.', 'cherry'],
            [7, 1, 1, 'I am sentence 2.', 'cherry']
        ], columns=['author', 'text_id', 'sentence_position', 'sentence', 'flavor'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_dataframes))
    def test_pipe_splits_into_sentences(self, df, expected_result):
        pipeline = pipes.SplitText(mock_nlp)

        result = pipeline(df)

        assert result.equals(expected_result)
