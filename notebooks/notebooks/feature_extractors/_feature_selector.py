from notebooks.feature_extractors import BaseFeatureExtractor


class FeatureSelector(BaseFeatureExtractor):
    def __init__(self, extractor, columns):
        self._extractor = extractor
        self._columns = columns

    def _extract(self, segments, show_loading):
        raw_features = self._extractor(segments)

        return raw_features[:, self._columns]
