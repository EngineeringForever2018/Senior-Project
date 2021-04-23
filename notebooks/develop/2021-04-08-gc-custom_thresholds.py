#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
random.seed(44)


# Thoughts: thresholds need to be custom to each profile. This would be a good opportunity to try to make a profile that gets more confident the more data about the author it has. The profile could model distributions of the differences between its sentences to its mean and other people's sentences to its mean. Then it can use these two distributions to determine which is more likely for incoming sentences. 
# 
# Question: Can euclidean distances from the mean or cosine similarites be treated as normal random variables?

# In[2]:


# Using function words for these experiments
function_words_train = pd.read_hdf(join(preprocess_path, "bawe_train_preprocessed_function_word_counter.hdf5"))
pos_bigrams_train = pd.read_hdf(join(preprocess_path, "bawe_train_preprocessed_pos2gram_counter.hdf5"))
function_words_train = pd.concat([function_words_train, pos_bigrams_train], axis=1)

function_words_train


# In[3]:


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


# In[4]:


filtered_train = select_good_features(function_words_train)

filtered_train


# In[5]:


std_train = (filtered_train - filtered_train.mean()) / filtered_train.std()

pca_vals, pca_vecs = np.linalg.eig(std_train.cov())
sorted_indices = np.flip(np.argsort(pca_vals))

components = pca_vecs[:, sorted_indices][:, :50]

std_train.dot(components)


# In[6]:


pd.concat([std_train.loc[0:1], std_train.loc[1:2]])
pca_train = std_train.dot(components)
lda_train = pca_train.loc[:50]


# In[7]:


lda_train.columns = np.arange(len(lda_train.columns))


# In[8]:


within_class = lda_train.groupby(level="author").cov().groupby(level=1).mean()

mean_diffs = lda_train.groupby(level="author").mean() - lda_train.mean()
between_class = mean_diffs.cov()

eig_matrix = np.dot(np.linalg.inv(within_class), between_class)

lda_vals, lda_vecs = np.linalg.eig(eig_matrix)
sorted_indices = np.flip(np.argsort(lda_vals))

lda_components = lda_vecs[:, sorted_indices][:, :15].real


# In[9]:


transformed = pca_train.dot(lda_components)
filtered_train = transformed
# transformed.index.get_level_values("author")


# In[10]:


# transformed.groupby(level="author").plot()
# plt.plot(transformed.to_numpy().T)

# plt.show()
# plt_matrix = transformed.to_numpy().T

# x_values = plt_matrix[0]
# y_values = plt_matrix[1]

plt.scatter(transformed[0], transformed[1], c=transformed.index.get_level_values("author"))
# plt.scatter(transformed[0], transformed[1], c=)
plt.show()
# x_values


# In[11]:


authors = filtered_train.index.get_level_values("author")
author_set = list(set(authors))

experiment_authors = random.sample(author_set, 10)

experiment_authors


# In[12]:


chosen_author = experiment_authors[9]

chosen_author_sentences = filtered_train.loc[chosen_author]

chosen_author_sentences


# Question: If I take the mean of each sentence distance and include it in the mean instead of excluding it, does this affect the mean/var distance?

# In[13]:


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


# Answer: Yes :(, the mean is consistently much lower because the sentence is included. This is unfortunate because the other method was much more efficient to compute.

# In[14]:


plt.hist(excluded_sentence_distances)

plt.show()


# Answer to previous question: Euclidean distances are not normal (no doy why would they be? euclidean distances from same distribution mean should on average be close to 0 and can't be lower than that).
# 
# Question: What if I just pick a threshold that accounts for 95% of the author's sentences.

# In[15]:


chosen_text = chosen_author_sentences.loc[0]

chosen_sentence_distances = get_excluded_sentence_distances(chosen_text.to_numpy())

index_threshold = math.floor(len(chosen_sentence_distances) * 0.75)
threshold = np.sort(chosen_sentence_distances)[index_threshold]

threshold, index_threshold


# In[16]:


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

