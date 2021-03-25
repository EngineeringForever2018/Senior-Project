from notebooks.feature_extractors import HeuristicExtractor
from notebooks.profiles import MahalanobisProfile


class StyleProfile(MahalanobisProfile):
    def __init__(self):
        super().__init__(HeuristicExtractor(4))
