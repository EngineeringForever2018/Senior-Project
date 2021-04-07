import os
from os.path import join
import pandas as pd
from pathlib import Path
import pdpipe as pdp
import sys
import numpy as np
from tqdm import tqdm

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir, extract_author_texts  # noqa

from notebooks import pipes
from notebooks.profiles import EuclideanProfile
from notebooks import benchmarking as bench
from notebooks.feature_extractors import HeuristicsExtractor
from notebooks.thresholders import SimpleAccuracyThresholder, SimpleThresholder

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))
outputs_path = join(project_root, 'outputs')

train_df = pd.read_hdf(join(preprocess_path, 'bawe_train_sentences.hdf5'))
valid_df = pd.read_hdf(join(preprocess_path, 'bawe_valid_sentences.hdf5'))

train_df = train_df.rename(columns={"sentence": "text"})
valid_df = valid_df.rename(columns={"sentence": "text"})

feature_extractors = [(HeuristicsExtractor(), "heuristics_extractor")]

profiles = [(EuclideanProfile(), "euclidean_distance_profile")]

thresholders = [(SimpleAccuracyThresholder(), "accuracy_thresholder"),
                (SimpleThresholder(bench.balanced_accuracies), "balanced_accuracy_thresholder")]

preprocessed_dfs = []

for feature_extractor, display_name in feature_extractors:
    train_path = join(preprocess_path, f"bawe_train_preprocessed_{display_name}.hdf5")
    valid_path = join(preprocess_path, f"bawe_valid_preprocessed_{display_name}.hdf5")

    preprocessed_train_exists = os.path.exists(train_path)
    preprocessed_valid_exists = os.path.exists(valid_path)

    if not (preprocessed_train_exists and preprocessed_valid_exists):
        print(f"Preprocessing train dataset for {display_name}", flush=True)
        preprocessed_train_df = feature_extractor(train_df, show_loading=True)
        print(f"Preprocessing valid dataset for {display_name}", flush=True)
        preprocessed_valid_df = feature_extractor(valid_df, show_loading=True)

        preprocessed_train_df.to_hdf(train_path, key=f"bawe_train_preprocessed_{display_name}")
        preprocessed_valid_df.to_hdf(valid_path, key=f"bawe_valid_preprocessed_{display_name}")
    else:
        preprocessed_train_df = pd.read_hdf(train_path)
        preprocessed_valid_df = pd.read_hdf(valid_path)

    preprocessed_dfs.append((preprocessed_train_df, preprocessed_valid_df, display_name))

def train_threshold(profile, df, thresholder):
    author_set = set(df.index.get_level_values(0))

    print("Training...", flush=True)
    distance_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        true_flags = distances.index.get_level_values(0) != author

        distance_sets.append(distances.to_numpy())
        true_flag_sets.append(true_flags)

    distances = np.concatenate(distance_sets)
    true_flags = np.concatenate(true_flag_sets)

    return thresholder(distances, true_flags)


def test_profile(profile, threshold, df):
    author_set = set(df.index.get_level_values(0))

    print("Testing...", flush=True)
    flag_sets = []
    true_flag_sets = []
    for author in tqdm(author_set):
        profile.reset()

        author_texts, rest_df = extract_author_texts(author, df)
        profile.feed(author_texts)
        distances = profile.distances(rest_df)

        flags = distances > threshold
        true_flags = distances.index.get_level_values(0) != author

        flag_sets.append(flags.to_numpy())
        true_flag_sets.append(true_flags)

    flags = np.concatenate(flag_sets)
    true_flags = np.concatenate(true_flag_sets)

    return [bench.balanced_accuracy(flags, true_flags)]


score_data = []
model_names = []

for profile, profile_name in profiles:
    for thresholder, thresholder_name in thresholders:
        for preprocessed_train_df, preprocessed_valid_df, extractor_name in preprocessed_dfs:
            threshold = train_threshold(profile, preprocessed_train_df, thresholder)
            profile.reset()

            scores = test_profile(profile, threshold, preprocessed_valid_df)
            score_data.append(scores)
            model_names.append(f"{profile_name}-{thresholder_name}-{extractor_name}")

results_df = pd.DataFrame(score_data, index=model_names, columns=["balanced_accuracy"])

results_df

preprocessed_dfs[0][0].index.get_level_values(0)

# pospca_extractor = OldPOSPCAExtractor(25, 10)
# pospca_profile = MahalanobisProfile(pospca_extractor)

heuristics_extractor = HeuristicExtractor(4)
heuristics_profile = MahalanobisProfile(heuristics_extractor)

pos2gram_extractor = OldPOS2GramExtractor(paragraph_length=1, best=20)
pos2gram_profile = MahalanobisProfile(pos2gram_extractor)

combined_extractor = ConcatExtractor(heuristics_extractor, pos2gram_extractor)
combined_profile = MahalanobisProfile(combined_extractor)

profiles = [heuristics_profile, pos2gram_profile, combined_profile]
profile_names = ['Heuristics', 'POS Bigrams', 'Combined']

benchmark_results = benchmark_profiles(grouped_valid_df, profiles,
                                       show_loading=True, names=profile_names, samples=20, authors_per_sample=5)

benchmark_results

benchmark_flags = benchmark_results.copy()

benchmark_flags[profile_names] = benchmark_flags[profile_names] < 0.85

benchmark_flags

positives_selection = benchmark_flags['flag']
negatives_selection = np.logical_not(benchmark_flags['flag'])

all_positives = positives_selection.sum()
all_negatives = negatives_selection.sum()

true_negatives = np.logical_not(benchmark_flags[negatives_selection][profile_names]).sum()
true_positives = benchmark_flags[positives_selection][profile_names].sum()

false_positives = np.logical_not(benchmark_flags[negatives_selection][profile_names]).sum()

sensitivity = true_positives / all_positives
specificity = true_negatives / all_negatives

precision = true_positives / (true_positives + false_positives)

balanced_accuracy = (sensitivity + specificity) / 2

train_benchmarks = pd.DataFrame(
    data=[balanced_accuracy, specificity, sensitivity, precision],
    index=['balanced accuracy', 'specificity', 'sensitivity (recall)',
           'precision']).T

train_benchmarks

train_benchmarks.to_hdf(join(outputs_path, 'bawe_train_benchmarks.hdf5'), key='bawe_train_benchmarks')

benchmark_flags[negatives_selection][profile_names].sum()

7 / (10)

benchmark_results.to_hdf(join(preprocess_path, 'benchmark_results.hdf5'), key='benchmark_results')

benchmark_results = pd.read_hdf(join(preprocess_path, 'benchmark_results.hdf5'))

benchmark_results
