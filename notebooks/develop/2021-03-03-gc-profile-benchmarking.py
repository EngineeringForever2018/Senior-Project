import os
from os.path import join
import pandas as pd
from pathlib import Path
import pdpipe as pdp
import sys
import numpy as np

project_root = Path('..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir  # noqa

from notebooks.benchmarking import benchmark_profiles  # noqa
from notebooks import pipes
from notebooks.profiles import MahalanobisProfile
from notebooks.feature_extractors import HeuristicExtractor, POS2GramExtractor, ConcatExtractor

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))
outputs_path = join(project_root, 'outputs')

train_df = pd.read_hdf(join(preprocess_path, 'bawe_train_sentences.hdf5'))
valid_df = pd.read_hdf(join(preprocess_path, 'bawe_valid_sentences.hdf5'))

pipeline = pipes.GroupSentences(n=50)

grouped_train_df = pipeline(train_df)

grouped_valid_df = pipeline(valid_df)

# pospca_extractor = POSPCAExtractor(25, 10)
# pospca_profile = MahalanobisProfile(pospca_extractor)

heuristics_extractor = HeuristicExtractor(4)
heuristics_profile = MahalanobisProfile(heuristics_extractor)

# pos2gram_extractor = POS2GramExtractor(paragraph_length=1)
# pos2gram_profile = MahalanobisProfile(pos2gram_extractor)

# combined_extractor = ConcatExtractor(heuristics_extractor, pos2gram_extractor)
# combined_profile = MahalanobisProfile(combined_extractor)

profiles = [heuristics_profile]
profile_names = ['Heuristics']

benchmark_results = benchmark_profiles(grouped_valid_df, profiles,
                                       show_loading=True, names=profile_names)

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
