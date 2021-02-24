#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import pdpipe as pdp
import spacy
import sys

from IPython.display import display
from os.path import join
from pathlib import Path

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir  # noqa

from notebooks import pipes  # noqa

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))

nlp = spacy.load('en_core_web_sm')

df = pd.read_hdf(join(preprocess_path, Path('bawe_df.hdf5')))


# # Information for the British Academic Written English Corpus
# 
# This notebook is for gathering information about the BAWE dataset. The dataset should already be parsed and stored in `data/preprocess/bawe_df.hdf5`.

# In[2]:


df


# In[3]:


resample_splits = False

train_df_path = join(preprocess_path, 'bawe_train_df.hdf5')
valid_df_path = join(preprocess_path, 'bawe_valid_df.hdf5')

train_df_exists = os.path.exists(train_df_path)
valid_df_exists = os.path.exists(valid_df_path)

if not (train_df_exists and valid_df_exists) or resample_splits:
    print('Resampling...')

    train_df = df.sample(frac=0.8).sort_values(by=['author', 'genre'])
    valid_df = df.drop(train_df.index)

    train_df = train_df.reset_index(drop=True)
    valid_df = valid_df.reset_index(drop=True)

    train_df.to_hdf(train_df_path, key='bawe_train_df')
    valid_df.to_hdf(valid_df_path, key='bawe_valid_df')
else:
    train_df = pd.read_hdf(train_df_path)
    valid_df = pd.read_hdf(valid_df_path)

print('Train Set:')
display(train_df)
print('Validation Set:')
display(valid_df)


# In[4]:


pipeline = pdp.PdPipeline([pipes.IDText(),
                           pipes.SplitText(nlp, show_loading=True)])

train_df = pipeline(train_df)
valid_df = pipeline(valid_df)

print('Train set:')
display(train_df)
print('Validation set:')
display(valid_df)


# In[5]:


train_df.to_hdf(join(preprocess_path, 'bawe_train_sentences.hdf5'),
                key='bawe_train_sentences')
valid_df.to_hdf(join(preprocess_path, 'bawe_valid_sentences.hdf5'),
                key='bawe_valid_sentences')


# In[10]:


237192 / 20

