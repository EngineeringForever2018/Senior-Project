from notebooks.feature_extractors import BaseFeatureExtractor
from typing import List


class FeatureConcatenator(BaseFeatureExtractor):
    def __init__(self, *feature_extractors):
        self._feature_extractors = feature_extractors

    def _segment_extract(self, segment: str) -> List[float]:
        return sum(
            [
                feature_extractor._segment_extract(segment)
                for feature_extractor in self._feature_extractors
            ],
            [],
        )
