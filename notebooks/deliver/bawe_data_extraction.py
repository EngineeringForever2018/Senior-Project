import os
from os.path import join
import pandas as pd
from pathlib import Path
import pickle
import spacy
import sys
from tqdm import tqdm

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir  # noqa

init_data_dir(project_root)

raw_path = Path('../data/raw')
preprocess_path = Path('../data/preprocess')
resources_path = Path('../resources')

nlp = spacy.load('en_core_web_sm')

def bawe_texts(filenames):
    # We use the plain text version of the corpus
    corpus_path = join(raw_path, Path('bawe/CORPUS_TXT'))

    for filename in tqdm(filenames):
        # The first 4 characters of the filename indicate the author, 5th
        # character indicates the genre.
        author = int(filename[:4])
        genre = filename[4]

        with open(join(corpus_path, filename), 'r') as f:
            text = f.read()

        yield author, genre, text

with open(join(resources_path, 'bawe_splits.p'), 'rb') as f:
    bawe_splits = pickle.load(f)
    train_filenames = bawe_splits['train']

df = pd.DataFrame(bawe_texts(train_filenames),
                  columns=['author', 'genre', 'text'])
df = df.sort_values(by=['author', 'genre']).reset_index(drop=True)

df

# print('Counting sentences...', flush=True)
# sentence_counts = [len(list(nlp(text).sents)) for text in tqdm(df['text'])]

# df['sentence_count'] = sentence_counts

# authors = set(df['author'])
# sentence_count = sum(sentence_counts)
# min_sentence_count = min(sentence_counts)
# max_sentence_count = max(sentence_counts)
# avg_sentence_count = sentence_count / len(sentence_counts)

# print(f'Author count: {len(authors)}')
# print(f'Sentence count: {sentence_count}')
# print(f'Minimum sentence count: {min_sentence_count}')
# print(f'Maximum sentence count: {max_sentence_count}')
# print(f'Average sentence count: {avg_sentence_count}')

# df

df.to_hdf(join(preprocess_path, 'bawe_df.hdf5'), key='bawe_df')
