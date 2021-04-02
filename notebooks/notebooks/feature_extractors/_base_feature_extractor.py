import numpy as np
import pandas as pd
from numpy import ndarray
from abc import ABC, abstractmethod
from typing import List


class BaseFeatureExtractor(ABC):
    """
    The base feature extractor class for concrete feature extractors to implement,
    concrete classes should only have to worry about extracting features from a single
    segment.
    """

    def __call__(self, segments) -> ndarray:
        """
        Turn :param segments into a feature matrix of size (n_segments, feature_dim)
        """
        if isinstance(segments, pd.DataFrame):
            return pd.DataFrame(
                [self._segment_extract(segment) for segment in segments["text"]],
                index=segments.index,
            )

        return np.array([self._segment_extract(segment) for segment in segments])

    @abstractmethod
    def _segment_extract(self, segment: str) -> List[float]:
        pass
