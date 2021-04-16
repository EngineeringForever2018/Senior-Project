from notebooks.feature_extractors import BaseSegmentExtractor
from typing import List


class Normalizer(BaseSegmentExtractor):
    def __init__(self, feature_extractor, count_extractor):
        self._feature_extractor = feature_extractor
        self._count_extractor = count_extractor

    def _segment_extract(self, segment: str) -> List[float]:
        segment_features = self._feature_extractor._segment_extract(segment)
        count = self._count_extractor._segment_extract(segment)[0]

        if count == 0:
            return segment_features

        return [segment_feature / count for segment_feature in segment_features]
