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
    doc.sents = (mock_sentence for mock_sentence in mock_sentences)  # noqa

    mock_tokens = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    for index in range(len(mock_tokens)):
        mock_tokens[index].pos_ = 'PUNCT'  # noqa

    doc.__iter__.return_value = (mock_token for mock_token in mock_tokens)

    return doc


def mock_nlp_iter():
    mock_tokens = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    for index in range(len(mock_tokens)):
        mock_tokens[index].pos_ = 'PUNCT'  # noqa

    return (mock_token for mock_token in mock_tokens)


# Should act like a spacy NLP object
mock_nlp = MagicMock(side_effect=mock_nlp_call)

# Should act like the POSVocab object
mock_vocab = MagicMock()
mock_vocab.__getitem__.return_value = 0


class TestIDText:
    dataframes = [
        pd.DataFrame([
            [5, 'I am example text'],
            [5, 'I am the second example text'],
            [8, 'Beep boop beep bibbity boop'],
            [8, 'Beep boop boop bop'],
            [8, 'Bop Bop']
        ], columns=['author', 'text'])
    ]

    expected_results = [
        pd.DataFrame([
            ['I am example text'],
            ['I am the second example text'],
            ['Beep boop beep bibbity boop'],
            ['Beep boop boop bop'],
            ['Bop Bop']
        ], index=pd.MultiIndex.from_tuples([(5, 0), (5, 1), (8, 0), (8, 1), (8, 2)], names=['author', 'text_id']),
            columns=['text'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_correct_indexing(self, df, expected_result):
        pipeline = pipes.IDText()

        result = pipeline(df)

        assert result.equals(expected_result)


class TestSplitText:
    dataframes = [
        pd.DataFrame([
            ['I am example text', 'blueberry'],
            ['I am another example text', 'cherry']
        ], index=pd.MultiIndex.from_tuples([(5, 0), (7, 0)], names=['author', 'text_id']),
            columns=['text', 'flavor'])
    ]

    expected_results = [
        pd.DataFrame([
            ['blueberry', 'I am sentence 1.'],
            ['blueberry', 'I am sentence 2.'],
            ['cherry', 'I am sentence 1.'],
            ['cherry', 'I am sentence 2.']
        ], index=pd.MultiIndex.from_tuples([(5, 0, 0), (5, 0, 1), (7, 0, 0), (7, 0, 1)],
                                           names=['author', 'text_id', 'sentence_position']),
            columns=['flavor', 'sentence'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pipe_splits_into_sentences(self, df, expected_result):
        pipeline = pipes.SplitText(mock_nlp)

        result = pipeline(df)

        assert result.equals(expected_result)


class TestGroupSentences:
    dataframes = [
        pd.DataFrame([
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 4.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 4.']
        ], index=pd.MultiIndex.from_tuples([
            (5, 0, 0),
            (5, 0, 1),
            (5, 0, 2),
            (5, 1, 0),
            (5, 1, 1),
            (5, 1, 2),
            (5, 1, 3),
            (7, 0, 0),
            (7, 0, 1),
            (7, 0, 2),
            (7, 0, 3)
        ], names=['author', 'text_id', 'sentence_position']),
            columns=['sentence'])
    ]

    expected_results = [
        pd.DataFrame([
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 4.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 4.']
        ], index=pd.MultiIndex.from_tuples([
            (5, 0, 0, 0),
            (5, 0, 0, 1),
            (5, 1, 0, 0),
            (5, 1, 0, 1),
            (5, 1, 1, 0),
            (5, 1, 1, 1),
            (7, 0, 0, 0),
            (7, 0, 0, 1),
            (7, 0, 1, 0),
            (7, 0, 1, 1)
        ], names=['author', 'text_id', 'group_position', 'sentence_position']),
            columns=['sentence'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pipe_groups_into_two(self, df, expected_result):
        pipeline = pipes.GroupSentences(n=2)

        result = pipeline(df)

        assert result.eq(expected_result).all().all()


class TestPOSTokenize:
    dataframes = [
        pd.DataFrame([
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 1.'],
            ['I am sentence 2.'],
            ['I am sentence 3.'],
            ['I am sentence 4.']
        ], index=pd.MultiIndex.from_tuples([ # noqa
            (5, 0, 0, 0),
            (5, 0, 0, 1),
            (5, 1, 0, 0),
            (5, 1, 0, 1),
            (7, 0, 0, 0),
            (7, 0, 0, 1),
            (7, 0, 1, 0),
            (7, 0, 1, 1)
        ], names=['author', 'text_id', 'group_position', 'sentence_position']),
            columns=['sentence'])
    ]

    expected_results = [
        pd.DataFrame([
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
            [[0, 0, 0, 0, 0], 5],
        ], index=pd.MultiIndex.from_tuples([ # noqa TODO: Maybe remove this duplication
            (5, 0, 0, 0),
            (5, 0, 0, 1),
            (5, 1, 0, 0),
            (5, 1, 0, 1),
            (7, 0, 0, 0),
            (7, 0, 0, 1),
            (7, 0, 1, 0),
            (7, 0, 1, 1)
        ], names=['author', 'text_id', 'group_position', 'sentence_position']),
        columns=['sentence', 'sentence_length'])
    ]

    @pytest.mark.parametrize('df, expected_result', zip(dataframes, expected_results))
    def test_pos_tokenize(self, df, expected_result):
        pipeline = pipes.POSTokenize(nlp=mock_nlp, pos_vocab=mock_vocab)

        result = pipeline(df)

        assert result.eq(expected_result).all().all()
