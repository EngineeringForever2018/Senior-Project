import pandas as pd
import pytest

from notebooks.datatools import AuthorDataset


class TestAuthorDataset:
    # dataframes = [
    #     pd.DataFrame([
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #         [[0, 1, 2, 3, 4], 5],
    #     ], index=pd.MultiIndex.from_tuples([ # noqa TODO
    #         (5, 0, 0, 0),
    #         (5, 0, 0, 1),
    #         (5, 1, 0, 0),
    #         (5, 1, 0, 1),
    #         (7, 0, 0, 0),
    #         (7, 0, 0, 1),
    #         (7, 0, 1, 0),
    #         (7, 0, 1, 1)
    #     ], names=['author', 'text_id', 'group_position', 'sentence_position']),
    #         columns=['sentence', 'sentence_length'])
    # ]

    dataframes = [
        pd.DataFrame([  # noqa TODO
            [[0, 1, 2], 3],
            [[0, 1, 2, 3], 4],
            [[0, 1], 2],
            [[0, 1, 2, 3, 4], 5],
            [[0, 1, 2], 3],
            [[0, 1, 2, 3], 4],
            [[0, 1], 2],
            [[0, 1, 2, 3, 4], 5]
        ], index=pd.MultiIndex.from_tuples([
            (5, 0, 0, 0),
            (5, 0, 0, 1),
            (7, 0, 1, 0),
            (7, 0, 1, 1),
            (8, 0, 0, 0),
            (8, 0, 0, 1),
            (12, 0, 1, 0),
            (12, 0, 1, 1)
        ], names=['author', 'text_id', 'group_position', 'sentence_position']),
            columns=['sentence', 'sentence_length'])
    ]

    # This comment is placed here to remind Gage of that time he managed to only test his code with in-order sequences,
    # leading to a very confusing bug with the real dataset that had random order. Hopefully next time Gage will not be
    # such a dumb ass.
    authors = [
        [7, 12],
        [5, 7],
        [7, 8]
    ]

    expected_results = [
        {'group_count': 2, 'author_count': 2, 'rows_per_author': [2, 2]}
    ]

    # TODO: Make this not just an entry point
    @pytest.mark.parametrize('df, authors, expected_result', zip(dataframes, authors, expected_results))
    def test_author_dataset_sampling(self, df, authors, expected_result):
        dataset = AuthorDataset(df)

        # while True:
        #     data = dataset.sample_authors(authors)
        #
        #     pass

        pass
