import pandas as pd
import pytest
import torch

from notebooks import pipes
from notebooks.datatools import AuthorDataset, EqualOpDataLoader


class TestEqualOpDataLoader:
    datasets = [
        AuthorDataset(pd.DataFrame([ # noqa TODO
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
            (7, 0, 0, 0),
            (7, 0, 0, 1),
            (8, 0, 0, 0),
            (8, 0, 0, 1),
            (12, 0, 0, 0),
            (12, 0, 0, 1)
        ], names=['author', 'text_id', 'group_position', 'sentence_position']),
            columns=['sentence', 'sentence_length']))
    ]

    @pytest.mark.parametrize('dataset', datasets)
    def test_entry_point(self, dataset):
        dl = EqualOpDataLoader(dataset, pipeline=pipes.PackSequence(torch.device(0)), bs=2)

        for batch in dl:
            pass
