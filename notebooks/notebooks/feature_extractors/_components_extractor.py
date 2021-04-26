from notebooks.feature_extractors import BaseFeatureExtractor
import pandas as pd
import numpy as np
from numpy import ndarray


class ComponentsExtractor(BaseFeatureExtractor):
    def __init__(self, extractor, components: ndarray):
        self._extractor = extractor
        self._components = components

    def _extract(self, segments: pd.DataFrame, show_loading: bool):
        raw_features = self._extractor(segments)

        return raw_features.dot(self._components)
