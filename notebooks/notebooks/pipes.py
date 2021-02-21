from itertools import chain, tee, repeat

from tqdm import tqdm

from notebooks.utils import split_into_sentences
import pandas as pd
from pdpipe import PdPipelineStage


class SplitText(PdPipelineStage):
    def __init__(self, nlp, show_loading=False):
        desc = 'A pipeline that will split texts from a dataframe into sentences.'
        super().__init__(desc=desc)
        self.nlp = nlp
        self.show_loading = show_loading

    def _prec(self, df):  # noqa
        return 'text' in df.columns

    def _transform(self, df, verbose):
        authors = []
        text_ids = []
        sentence_positions = []
        sentences = []

        if self.show_loading:
            rows = tqdm(df.itertuples())
        else:
            rows = df.itertuples()

        for row in rows:
            row_authors, row_text_ids, row_sentence_positions, row_sentences = self._split_row(row)

            authors.append(row_authors)
            text_ids.append(row_text_ids)
            sentence_positions.append(row_sentence_positions)
            sentences.append(row_sentences)

        authors = chain(*authors)
        text_ids = chain(*text_ids)
        sentence_positions = chain(*sentence_positions)
        sentences = chain(*sentences)

        col_dict = {'author': list(authors), 'text_id': list(text_ids), 'sentence_position': list(sentence_positions),
                    'sentence': list(sentences)}

        return pd.DataFrame(col_dict)

    def _split_row(self, row):
        sentences = split_into_sentences(row.text, nlp=self.nlp)
        sentences, sentences_copy = tee(sentences)
        sentence_count = len(list(sentences_copy))

        authors = repeat(row.author, times=sentence_count)
        text_ids = repeat(row.Index, times=sentence_count)
        sentence_positions = (position for position, _ in enumerate(range(sentence_count)))

        return authors, text_ids, sentence_positions, sentences


class GroupSentences(PdPipelineStage):
    def __init__(self, n):
        desc = 'A pipeline that will group sentences from a dataframe into ordered groups of n.'
        super().__init__(desc=desc)
        self.n = n

    def _prec(self, df): # noqa
        return True

    def _transform(self, df, verbose):
        def group_sentences(text_group):
            sentence_positions = text_group['sentence_position']
            result = text_group.copy()

            # Just integer divide by the group length. If the sentence positions are [0, 1, 2, 3], and the group length
            # is 2, then the resulting group positions would be [0, 0, 1, 1], which is desirable.
            result['group_position'] = (sentence_positions / self.n).astype(int)
            result['sentence_position'] -= result['group_position'] * self.n

            last_sentence_position = max(sentence_positions)
            remainder = (last_sentence_position + 1) % self.n
            max_sentence_position = last_sentence_position - remainder

            # Wherever the sentence position is greater than the max sentence position, we need to replace group with
            # -1 (which means we're going to drop those rows later).
            result['group_position'][sentence_positions > max_sentence_position] = -1

            return result

        df = df.groupby('text_id').apply(group_sentences)

        df = df[df['group_position'] != -1]

        return df.reset_index(drop=True)

