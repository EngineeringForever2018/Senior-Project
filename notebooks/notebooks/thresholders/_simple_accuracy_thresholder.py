from notebooks.thresholders import SimpleThresholder
from notebooks import benchmarking as bench


class SimpleAccuracyThresholder(SimpleThresholder):
    """
    A SimpleThresholder that uses accuracy as its benchmarking function.
    """

    def __init__(self):
        super().__init__(bench.correct_counts)
