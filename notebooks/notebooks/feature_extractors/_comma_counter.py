from notebooks.feature_extractors import BaseFeatureExtractor
from typing import List


class CommaCounter(BaseFeatureExtractor):
    """Extracts the number of commas from each segment."""

    def _segment_extract(self, segment: str) -> List[float]:
        return [float(segment.count(","))]
