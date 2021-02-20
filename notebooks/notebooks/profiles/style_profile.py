from notebooks.feature_extractors import POSPCAExtractor
from notebooks.profiles import MahalanobisProfile


class StyleProfile(MahalanobisProfile):
    def __init__(self):
        super().__init__(POSPCAExtractor(1, 10))
