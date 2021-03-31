from notebooks.feature_extractors import BaseFeatureExtractor
from typing import List


class WordCounter(BaseFeatureExtractor):
    def _segment_extract(self, segment: str) -> List[float]:
        return [float(len(segment.split()))]
