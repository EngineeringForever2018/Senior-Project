import pandas as pd
import numpy as np
from pathlib import Path
from os.path import join
from tqdm import tqdm
import random
from matplotlib import pyplot as plt
import math

project_root = Path('..')

preprocess_path = join(project_root, Path('data/preprocess'))
random.seed(10)

# Using function words for these experiments
function_words_train = pd.read_hdf(join(preprocess_path, "bawe_train_preprocessed_function_word_counter.hdf5"))
pos_bigrams_train = pd.read_hdf(join(preprocess_path, "bawe_train_preprocessed_pos2gram_counter.hdf5"))
function_words_train = pd.concat([function_words_train, pos_bigrams_train], axis=1)

function_words_train

def select_good_features(df):
    overall_var = df.var()

    author_vars = df.groupby(level="author").var()

    mean_explained_var = (overall_var - author_vars).mean()

    # Features that reduce the variance within classes should hopefully be good
    # features.
    selections = mean_explained_var > 0

    # The index of selctions should be the columns of the dataframe given the
    # last few operations.
    chosen_columns = selections[selections].index.tolist()

    return df[chosen_columns]

filtered_train = select_good_features(function_words_train)

filtered_train

authors = filtered_train.index.get_level_values("author")
author_set = list(set(authors))

experiment_authors = random.sample(author_set, 5)

experiment_authors

chosen_author = experiment_authors[2]

chosen_author_sentences = filtered_train.loc[chosen_author]

chosen_author_sentences

included_sentences_distances = np.linalg.norm(chosen_author_sentences - chosen_author_sentences.mean(), axis=1)

included_sentences_distances_mean = included_sentences_distances.mean()
included_sentences_distances_var = included_sentences_distances.var()


def get_excluded_sentence_distances(array):
    def sentence_distance(i):
        selection = [True] * len(array)
        selection[i] = False
        return np.linalg.norm(array[i] - np.mean(array[selection]))

    return np.array([sentence_distance(index) for index in range(len(array))])


excluded_sentence_distances = get_excluded_sentence_distances(chosen_author_sentences.to_numpy())

excluded_sentence_distances_mean = excluded_sentence_distances.mean()
excluded_sentence_distances_var = excluded_sentence_distances.var()

included_sentences_distances_mean, excluded_sentence_distances_mean

plt.hist(excluded_sentence_distances)

plt.show()

chosen_text = chosen_author_sentences.loc[0]

chosen_sentence_distances = get_excluded_sentence_distances(chosen_text.to_numpy())

index_threshold = math.floor(len(chosen_sentence_distances) * 0.6)
threshold = np.sort(chosen_sentence_distances)[index_threshold]

threshold, index_threshold

def euclidean_distance(mean, df):
    return np.linalg.norm(mean - df, axis=1)


chosen_text_mean = chosen_text.mean()

same_texts = chosen_author_sentences.drop(index=(0,))
other_author_texts = filtered_train.drop(index=(chosen_author,))

same_sentence_classifications = pd.DataFrame(
    euclidean_distance(chosen_text_mean, same_texts) > threshold, index=same_texts.index
)
other_sentence_classifications = pd.DataFrame(
    euclidean_distance(chosen_text_mean, other_author_texts) > threshold, index=other_author_texts.index
)

same_text_classifications = same_sentence_classifications.groupby(level=("text_id")).mean() > 0.5
other_text_classifications = other_sentence_classifications.groupby(level=("author", "text_id")).mean() > 0.5

same_flags = same_text_classifications.sum()
same_length = len(same_text_classifications)
other_flags = other_text_classifications.sum()
other_length = len(other_text_classifications)

tnr = (same_length - same_flags) / same_length
tpr = other_flags / other_length

tnr[0], tpr[0]
