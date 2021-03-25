import random

import pandas as pd
from tqdm import tqdm


def texts_from_author(dataset, author):
    author_data = dataset.loc[author]

    author_texts_df = author_data.groupby("text_id")

    def sentences_to_text(group):
        group = group.sort_values(by=["group_position", "sentence_position"])

        text = "".join(group["sentence"].tolist())

        return text

    author_texts_df = author_texts_df.apply(sentences_to_text)

    return author_texts_df.tolist()


def texts_from_authors(dataset, authors):
    return [texts_from_author(dataset, author) for author in authors]


def old_benchmark_profiles(
    dataset, profiles, authors_per_sample=30, samples=10, show_loading=False, names=None
):
    authors = list(zip(*dataset.index.tolist()))[0]
    authors = set(authors)

    data = []

    samples_iter = range(samples)
    if show_loading:
        samples_iter = tqdm(samples_iter)

    for _ in samples_iter:
        selection = random.sample(authors, k=authors_per_sample)
        texts = texts_from_authors(dataset, selection)

        assert len(texts) == authors_per_sample
        assert isinstance(texts[0][0], str)

        profile_author, profile_texts = selection[0], texts[0]
        other_authors, other_texts = selection[1:], texts[1:]
        # Sum each list of texts together so that it is one big list
        other_texts = sum(other_texts, [])
        assert isinstance(other_texts[0], str)

        if len(profile_texts) == 1:
            profile_suspects = []

            # Just use this single text for the profile
            for profile in profiles:
                profile.feed(profile_texts[0])
        else:
            # There should be more than one text, otherwise this author shouldn't be in the dataset
            profile_suspects = [profile_texts[-1]]
            profile_texts = profile_texts[:-1]

            # TODO: Duplicate code, for either empty or non empty profile_texts sum all and feed to profiles
            # Sum texts together into one string to feed to the profiles
            profile_all_text = "".join(profile_texts)

            for profile in profiles:
                profile.feed(profile_all_text)

        for suspect in profile_suspects:
            scores = [profile.score(suspect) for profile in profiles]

            data.append([False] + scores)

        for suspect in other_texts:
            scores = [profile.score(suspect) for profile in profiles]

            data.append([True] + scores)

        for profile in profiles:
            profile.reset()

    if names is None:
        names = [str(num) for num, _ in enumerate(profiles)]

    columns = ["flag"] + names

    return pd.DataFrame(columns=columns, data=data)


def benchmark_profiles(
    dataset, profiles, authors_per_sample=30, samples=10, show_loading=False, names=None
):
    authors = list(zip(*dataset.index.tolist()))[0]
    authors = set(authors)

    data = []

    samples_iter = range(samples)
    if show_loading:
        samples_iter = tqdm(samples_iter)

    for _ in samples_iter:
        selection = random.sample(authors, k=authors_per_sample)
        texts = texts_from_authors(dataset, selection)

        assert len(texts) == authors_per_sample
        assert isinstance(texts[0][0], str)

        profile_author, profile_texts = selection[0], texts[0]
        other_authors, other_texts = selection[1:], texts[1:]
        # Sum each list of texts together so that it is one big list
        other_texts = sum(other_texts, [])
        assert isinstance(other_texts[0], str)

        if len(profile_texts) == 1:
            profile_suspects = []

            # Just use this single text for the profile
            for profile in profiles:
                profile.feed(profile_texts[0])
        else:
            # There should be more than one text, otherwise this author shouldn't be in the dataset
            profile_suspects = [profile_texts[-1]]
            profile_texts = profile_texts[:-1]

            # TODO: Duplicate code, for either empty or non empty profile_texts sum all and feed to profiles
            # Sum texts together into one string to feed to the profiles
            profile_all_text = "".join(profile_texts)

            for profile in profiles:
                profile.feed(profile_all_text)

        for suspect in profile_suspects:
            scores = [profile.score(suspect) for profile in profiles]

            data.append([False] + scores)

        for suspect in other_texts:
            scores = [profile.score(suspect) for profile in profiles]

            data.append([True] + scores)

        for profile in profiles:
            profile.reset()

    if names is None:
        names = [str(num) for num, _ in enumerate(profiles)]

    columns = ["flag"] + names

    return pd.DataFrame(columns=columns, data=data)
