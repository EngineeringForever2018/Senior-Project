import os
from os.path import join
import pandas as pd
from pathlib import Path
import sys

project_root = Path('../..')
sys.path.append(os.path.abspath(project_root))
from notebooks.utils import init_data_dir  # noqa

# from notebooks.benchmarking import benchmark_profiles  # noqa

init_data_dir(project_root)

preprocess_path = join(project_root, Path('data/preprocess'))
outputs_path = join(project_root, 'outputs')

benchmark_results = pd.read_hdf(join(outputs_path,
                                     'bawe_train_benchmarks.hdf5'))

benchmark_results
