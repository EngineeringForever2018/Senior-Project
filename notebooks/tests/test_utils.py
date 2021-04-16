import pytest
import pandas as pd
from notebooks import utils
from tests import tutils


# TODO: Edge cases.
# TODO: Error conditons (good error reporting when not enough texts are available).
# class TestExtractAuthorTexts:
#     example_dataframe = pd.DataFrame(
#         [
#             [1.0, 2.0],
#             [2.0, 3.0],
#             [1.0, 2.0],
#             [3.0, 4.0],
#             [5.0, 6.0],
#             [1.0, 2.0],
#             [3.0, 4.0],
#             [1.0, 2.0],
#             [3.0, 4.0],
#             [1.0, 2.0],
#         ],
#         index=pd.MultiIndex.from_tuples(
#             [
#                 (7, 0, 0),
#                 (7, 0, 1),
#                 (7, 1, 0),
#                 (7, 1, 1),
#                 (7, 1, 2),
#                 (13, 0, 0),
#                 (13, 0, 1),
#                 (13, 1, 0),
#                 (13, 1, 1),
#                 (13, 2, 0),
#             ],
#             names=["author", "text_id", "sentence_id"],
#         ),
#     )
# 
#     authors = [7, 13]
# 
#     dataframes = [
#         example_dataframe.copy(),
#         example_dataframe.copy(),
#     ]
# 
#     text_counts = [1, 2]
# 
#     expected_author_text_sets = [
#         pd.DataFrame(
#             [
#                 [1.0, 2.0],
#                 [2.0, 3.0],
#             ],
#             index=pd.MultiIndex.from_tuples(
#                 [
#                     (7, 0, 0),
#                     (7, 0, 1),
#                 ],
#                 names=["author", "text_id", "sentence_id"],
#             ),
#         ),
#         pd.DataFrame(
#             [
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#             ],
#             index=pd.MultiIndex.from_tuples(
#                 [
#                     (8, 0, 0),
#                     (8, 0, 1),
#                 ],
#                 names=["author", "text_id", "sentence_id"],
#             ),
#         ),
#     ]
# 
#     expected_dataframes = [
#         pd.DataFrame(
#             [
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#                 [5.0, 6.0],
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#                 [1.0, 2.0],
#             ],
#             index=pd.MultiIndex.from_tuples(
#                 [
#                     (7, 1, 0),
#                     (7, 1, 1),
#                     (7, 1, 2),
#                     (13, 0, 0),
#                     (13, 0, 1),
#                     (13, 1, 0),
#                     (13, 1, 1),
#                     (13, 2, 0),
#                 ],
#                 names=["author", "text_id", "sentence_id"],
#             ),
#         ),
#         pd.DataFrame(
#             [
#                 [1.0, 2.0],
#                 [2.0, 3.0],
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#                 [5.0, 6.0],
#                 [1.0, 2.0],
#                 [3.0, 4.0],
#                 [1.0, 2.0],
#             ],
#             index=pd.MultiIndex.from_tuples(
#                 [
#                     (7, 0, 0),
#                     (7, 0, 1),
#                     (7, 1, 0),
#                     (7, 1, 1),
#                     (7, 1, 2),
#                     (13, 1, 0),
#                     (13, 1, 1),
#                     (13, 2, 0),
#                 ],
#                 names=["author", "text_id", "sentence_id"],
#             ),
#         ),
#     ]
# 
#     @pytest.mark.parametrize(
#         "author, df, expected_author_texts, expected_dataframe",
#         zip(authors, dataframes, expected_author_text_sets, expected_dataframes),
#     )
#     def test_extract_author_tests_should_return_author_texts(
#         self, author, df, expected_author_texts, expected_dataframe
#     ):
#         author_texts, df = utils.extract_author_texts(author, df)
# 
#         assert tutils.npequal(author_texts, expected_author_texts)
#         assert tutils.npequal(df, expected_dataframe)
