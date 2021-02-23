import numpy as np


class AuthorDataset:
    def __init__(self, df):
        self.df = df

    def sample_authors(self, authors):
        texts = self.df.loc[authors]

        def get_max_text_id(text_group):
            _, group_text_ids, _, _ = zip(*text_group.index.tolist())

            return max(group_text_ids)

        max_text_ids = texts.groupby('author').apply(get_max_text_id) + 1
        max_text_id = max(max_text_ids)

        text_ids = np.random.randint(max_text_id, size=len(authors)) % max_text_ids
        text_ids = text_ids.tolist()

        # groups = self.df.loc[list(zip(authors, text_ids)), :, :]
        groups = self.df[self.df.index.droplevel(['group_position', 'sentence_position']).isin(zip(authors, text_ids))]

        def get_max_group_position(group):
            _, _, group_group_positions, _ = zip(*group.index.tolist())

            return max(group_group_positions)

        max_group_positions = groups.groupby(['author', 'text_id']).apply(get_max_group_position) + 1
        max_group_position = max(max_group_positions)

        group_positions = np.random.randint(max_group_position, size=len(authors)) % max_group_positions
        group_positions = group_positions.tolist()

        selection = self.df.index.droplevel('sentence_position').isin(zip(authors, text_ids, group_positions))
        return self.df[selection]
