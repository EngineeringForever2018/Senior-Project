from notebooks.feature_extractors import BaseSegmentExtractor
from typing import List


class WordCounter(BaseSegmentExtractor):
    def _segment_extract(self, segment: str) -> List[float]:
        return [float(len(segment.split()))]
