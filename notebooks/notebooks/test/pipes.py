from unittest.mock import MagicMock

import pandas as pd
import pytest

from notebooks import pipes


# Mocks
def mock_nlp_call(text):
    mock_sentences = [MagicMock(), MagicMock()]
    mock_sentences[0].text = 'I am sentence 1.'
    mock_sentences[1].text = 'I am sentence 2.'

    doc = MagicMock()
    doc.sents = (mock_sentence for mock_sentence in mock_sentences) # noqa

    mock_tokens = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    for index in range(len(mock_tokens)):
        mock_tokens[index].pos_ = 'PUNCT'  # noqa

    doc.__iter__.return_value = (mock_token for mock_token in mock_tokens)

    return doc


def mock_nlp_iter():
    mock_tokens = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    for index in range(len(mock_tokens)):
        mock_tokens[index].pos_ = 'PUNCT' # noqa

    return (mock_token for mock_token in mock_tokens)


# Should act like a spacy NLP object
mock_nlp = MagicMock(side_effect=mock_nlp_call)


# Should act like the POSVocab object
mock_vocab = MagicMock()
mock_vocab.__getitem__.return_value = 0


class TestSplitText:
    dataframes = [
        pd.DataFrame([
            [5, 'I am example text', 'blueberry'],
            [7, 'I am another example text', 'cherry']
        ], columns=['author', 'text', 'flavor'])
    ]

    # TODO: Have pipeline keep other columns
    # expected_dataframes = [
    #     pd.DataFrame([
    #         [5, 0, 0, 'I am sentence 1.', 'blueberry'],
    #         [5, 0, 1, 'I am sentence 2.', 'blueberry'],
    #         [7, 1, 0, 'I am sentence 1.', 'cherry'],
    #         [7, 1, 1, 'I am sentence 2.', 'cherry']
    #     ], columns=['author', 'text_id', 'sentence_position', 'sentence', 'flavor'])
    # ]

    expected_results = [
        pd.DataFrame([
            [5, 0, 0, 'I am sentence 1.'],
            [5, 0, 1, 'I am sentence 2.'],
            [7, 1, 0, 'I am sentence 1.'],
            [7, 1, 1, 'I am sentence 2.']
        ], columns=['author', 'text_id', 'sentence_position', 'sentence'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pipe_splits_into_sentences(self, df, expected_result):
        pipeline = pipes.SplitText(mock_nlp)

        result = pipeline(df)

        assert result.equals(expected_result)


class TestGroupSentences:
    dataframes = [
        pd.DataFrame([
            [5, 0, 0, 'I am sentence 1.'],
            [5, 0, 1, 'I am sentence 2.'],
            [5, 0, 2, 'I am sentence 3.'],
            [5, 1, 0, 'I am sentence 1.'],
            [5, 1, 1, 'I am sentence 2.'],
            [5, 1, 2, 'I am sentence 3.'],
            [5, 1, 3, 'I am sentence 4.'],
            [7, 2, 0, 'I am sentence 1.'],
            [7, 2, 1, 'I am sentence 2.'],
            [7, 2, 2, 'I am sentence 3.'],
            [7, 2, 3, 'I am sentence 4.']
        ], columns=['author', 'text_id', 'sentence_position', 'sentence'])
    ]

    expected_results = [
        pd.DataFrame([
            [5, 0, 0, 0, 'I am sentence 1.'],
            [5, 0, 0, 1, 'I am sentence 2.'],
            [5, 1, 0, 0, 'I am sentence 1.'],
            [5, 1, 0, 1, 'I am sentence 2.'],
            [5, 1, 1, 0, 'I am sentence 3.'],
            [5, 1, 1, 1, 'I am sentence 4.'],
            [7, 2, 0, 0, 'I am sentence 1.'],
            [7, 2, 0, 1, 'I am sentence 2.'],
            [7, 2, 1, 0, 'I am sentence 3.'],
            [7, 2, 1, 1, 'I am sentence 4.']
        ], columns=['author', 'text_id', 'group_position', 'sentence_position', 'sentence'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pipe_groups_into_two(self, df, expected_result):
        pipeline = pipes.GroupSentences(n=2)

        result = pipeline(df)

        assert result.eq(expected_result).all().all()


class TestPOSTokenize:
    dataframes = [
        pd.DataFrame([
            [5, 0, 0, 0, 'I am sentence 1.'],
            [5, 0, 0, 1, 'I am sentence 2.'],
            [5, 1, 0, 0, 'I am sentence 1.'],
            [5, 1, 0, 1, 'I am sentence 2.'],
            [7, 2, 0, 0, 'I am sentence 1.'],
            [7, 2, 0, 1, 'I am sentence 2.'],
            [7, 2, 1, 0, 'I am sentence 3.'],
            [7, 2, 1, 1, 'I am sentence 4.']
        ], columns=['author', 'text_id', 'group_position', 'sentence_position', 'sentence'])
    ]

    expected_results = [
        pd.DataFrame([
            [5, 0, 0, 0, [0, 0, 0, 0, 0], 5],
            [5, 0, 0, 1, [0, 0, 0, 0, 0], 5],
            [5, 1, 0, 0, [0, 0, 0, 0, 0], 5],
            [5, 1, 0, 1, [0, 0, 0, 0, 0], 5],
            [7, 2, 0, 0, [0, 0, 0, 0, 0], 5],
            [7, 2, 0, 1, [0, 0, 0, 0, 0], 5],
            [7, 2, 1, 0, [0, 0, 0, 0, 0], 5],
            [7, 2, 1, 1, [0, 0, 0, 0, 0], 5],
        ], columns=['author', 'text_id', 'group_position', 'sentence_position', 'sentence', 'sentence_length'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pos_tokenize(self, df, expected_result):
        pipeline = pipes.POSTokenize(nlp=mock_nlp, pos_vocab=mock_vocab)

        result = pipeline(df)

        assert result.eq(expected_result).all().all()
