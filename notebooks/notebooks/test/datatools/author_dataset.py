import pandas as pd
import pytest

from notebooks.datatools import AuthorDataset


class TestAuthorDataset:
    dataframes = [
        pd.DataFrame([
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2, 3, 4], 5],
        ], index=pd.MultiIndex.from_tuples([ # noqa TODO
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

    authors = [
        [5, 7]
    ]

    expected_results = [
        {'group_count': 2, 'author_count': 2, 'rows_per_author': [2, 2]}
    ]

    @pytest.mark.parametrize('df, authors, expected_result', zip(dataframes, authors, expected_results))
    def test_author_dataset_sampling(self, df, authors, expected_result):
        dataset = AuthorDataset(df)

        data = dataset.sample_authors(authors)

        pass
