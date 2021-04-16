from notebooks.feature_extractors import BaseSegmentExtractor
from typing import List


class CommaCounter(BaseSegmentExtractor):
    """Extracts the number of commas from each segment."""

    def _segment_extract(self, segment: str) -> List[float]:
        return [float(segment.count(","))]
