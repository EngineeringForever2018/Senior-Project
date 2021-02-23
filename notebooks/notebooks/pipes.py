from itertools import chain, tee, repeat

import numpy as np
from tqdm import tqdm

from notebooks.utils import split_into_sentences, tokenize, pos_tag
import pandas as pd
from pdpipe import PdPipelineStage


class IDText(PdPipelineStage):
    def __init__(self):
        super().__init__()

    def _prec(self, df):  # noqa
        return True

    def _transform(self, df, verbose):
        def id_text(df_group):
            result = df_group.copy()
            text_count = len(result['text'])

            result['text_id'] = np.arange(text_count)

            return result

        df = df.groupby('author').apply(id_text)

        new_df = pd.DataFrame(df['text'].copy(), columns=['text'])
        new_df.index = pd.MultiIndex.from_frame(df[['author', 'text_id']])

        return new_df


class SplitText(PdPipelineStage):
    def __init__(self, nlp, show_loading=False):
        desc = 'A pipeline that will split texts from a dataframe into sentences.'
        super().__init__(desc=desc)
        self.nlp = nlp
        self.show_loading = show_loading

    def _prec(self, df):  # noqa
        return 'text' in df.columns

    def _transform(self, df, verbose):
        if self.show_loading:
            progress_bar = tqdm(total=len(df))

        def split_text(row):
            sentences = list(split_into_sentences(row['text'].iloc[0], nlp=self.nlp))

            new_row = row.drop(columns=['text']).copy()

            new_row['sentence'] = [sentences]
            new_row = new_row.explode('sentence', ignore_index=True)

            new_row.index = pd.MultiIndex.from_tuples(zip(new_row.index), names=['sentence_position'])

            if self.show_loading:
                progress_bar.update()

            return new_row

        new_df = df.groupby(['author', 'text_id']).apply(split_text)

        return new_df


class POSTokenize(PdPipelineStage):
    def __init__(self, nlp, pos_vocab):
        desc = 'A pipeline that will split sentences into tokens and then replace each token with a POS tag.'
        super().__init__(desc=desc)
        self.tokenize = Tokenize(nlp=nlp)
        self.pos_tag = POSTag(pos_vocab=pos_vocab)

    def _prec(self, df):  # noqa
        return True

    def _transform(self, df, verbose):
        df = self.tokenize(df)
        df = self.pos_tag(df)

        df['sentence_length'] = [len(sentence) for sentence in df['sentence']]

        return df


class GroupSentences(PdPipelineStage):
    def __init__(self, n):
        desc = 'A pipeline that will group sentences from a dataframe into ordered groups of n.'
        super().__init__(desc=desc)
        self.n = n

    def _prec(self, df):  # noqa
        return True

    def _transform(self, df, verbose):
        def group_sentences(text_group):
            _, _, sentence_positions = zip(*text_group.index.tolist())
            sentence_positions = np.array(sentence_positions)
            result = text_group.copy()

            # Just integer divide by the group length. If the sentence positions are [0, 1, 2, 3], and the group length
            # is 2, then the resulting group positions would be [0, 0, 1, 1], which is desirable.
            # result['group_position'] = (sentence_positions / self.n).astype(int)
            group_positions = (sentence_positions / self.n).astype(int)
            # result['sentence_position'] -= result['group_position'] * self.n
            new_sentence_positions = sentence_positions - (group_positions * self.n)

            last_sentence_position = max(sentence_positions)
            remainder = (last_sentence_position + 1) % self.n
            max_sentence_position = last_sentence_position - remainder

            # Wherever the sentence position is greater than the max sentence position, we need to replace group with
            # -1 (which means we're going to drop those rows later).
            group_positions[sentence_positions > max_sentence_position] = -1

            result.index = pd.MultiIndex.from_tuples(zip(group_positions, new_sentence_positions),
                                                     names=['group_position', 'sentence_position'])

            return result

        df = df.groupby(['author', 'text_id']).apply(group_sentences)

        df = df.query('group_position != -1')

        return df


class POSTag(PdPipelineStage):
    def __init__(self, pos_vocab):
        desc = 'A pipeline that will tag tokens with their POS.'
        super().__init__(desc=desc)
        self.pos_vocab = pos_vocab

    def _prec(self, df):  # noqa
        return True

    def _transform(self, df, verbose):
        df = df.copy()

        df['sentence'] = [pos_tag(sentence, pos_vocab=self.pos_vocab) for sentence in df['sentence']]

        return df


class Tokenize(PdPipelineStage):
    def __init__(self, nlp):
        desc = 'A pipeline that will split sentences into tokens.'
        super().__init__(desc=desc)
        self.nlp = nlp

    def _prec(self, df):  # noqa
        return True

    def _transform(self, df, verbose):
        df = df.copy()

        df['sentence'] = [tokenize(sentence, nlp=self.nlp) for sentence in df['sentence']]

        return df
