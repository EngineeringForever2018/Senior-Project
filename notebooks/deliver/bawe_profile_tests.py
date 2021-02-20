import os
from os.path import join
from pathlib import Path
import torch
from tqdm import tqdm
import random
import pandas as pd

import sys

sys.path.append(os.path.abspath(Path('..')))

from notebooks.profiles import MahalanobisProfile
from notebooks.feature_extractors import POSPCAExtractor, HeuristicExtractor

bawe_group_dir = Path('../data/preprocess/bawe-group')

def test_profile(profile, cutoff):
    ids = os.listdir(bawe_group_dir)
    other_ids = ids.copy()
    random.shuffle(ids)
    random.shuffle(other_ids)

    irrelevant, false_positives, relevant, true_positives = 0, 0, 0, 0
    # For performance reasons, only choose 5 authors
    for id in ids[:10]:
        profile.reset()
        texts = file_texts(id)

        first_text = texts[0]
        other_texts = texts[1:]

        # This author's first essay is used to profile that author
        profile.feed(first_text)

        # The rest of their essays are tested against this profile
        other_scores = torch.tensor([profile.score(text) for text in other_texts])

        irrelevant += len(texts)
        false_positives += sum(other_scores < cutoff)

        # Compare this author to 20 random different authors
        new_relevant, new_true_positives = grade_others(profile, other_ids[:30], id, cutoff)
        relevant += new_relevant
        true_positives += new_true_positives

    # Precision is relevant selections out of all selections
    precision = true_positives / (true_positives + false_positives)
    # Recall is all relevant selections out of all relevant items
    recall = true_positives / relevant

    false_negatives = relevant - true_positives

    # False positives and false negatives sum to the error count, and
    # irrelevant and relevant items sum to the whole set
    error_rate = false_negatives + false_positives / (irrelevant + relevant)

    return float(precision), float(recall), float(error_rate)


def file_texts(id):
    filenames = os.listdir(join(bawe_group_dir, id))
    texts = []
    for filename in filenames:
        with open(join(bawe_group_dir, f'{id}/{filename}'), 'r') as f:
            texts.append(f.read())

    return texts


def grade_others(profile, ids, id, cutoff):
    rest_ids = [other_id for other_id in ids if other_id != id]

    relevant, true_positives = 0, 0
    for other_id in tqdm(rest_ids):
        texts = file_texts(other_id)

        scores = torch.tensor([profile.score(text) for text in texts])

        true_positives += sum(scores < cutoff)
        relevant += len(texts)

    return relevant, true_positives

pospca_extractor = POSPCAExtractor(4, 10)
pospca_profile = MahalanobisProfile(pospca_extractor)

pospca_precision, pospca_recall, pospca_error = test_profile(pospca_profile, 0.50)

heuristics_extractor = HeuristicExtractor(4)
heuristics_profile = MahalanobisProfile(heuristics_extractor)

heuristics_precision, heuristics_recall, heuristics_error = test_profile(heuristics_profile, 0.90)

metric_data = [
    [pospca_precision, pospca_recall, pospca_error],
    [heuristics_precision, heuristics_recall, heuristics_error]
]

pd.DataFrame(metric_data, columns=['Precision', 'Recall', 'Error'], index=['POSPCA', 'Heuristics'])
