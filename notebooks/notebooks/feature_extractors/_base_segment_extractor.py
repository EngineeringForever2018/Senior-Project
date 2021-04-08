import numpy as np
from tqdm import tqdm
import pandas as pd
from numpy import ndarray
from notebooks.feature_extractors import BaseFeatureExtractor
from typing import List
from abc import abstractmethod


# TODO: Refactor this so that it only requires extract to be defined, and then make a
#       separate BaseSegmentExtractor that implements this class with template methods.
class BaseSegmentExtractor(BaseFeatureExtractor):
    """
    The base feature extractor class for concrete feature extractors to implement,
    concrete classes should only have to worry about extracting features from a single
    segment.
    """

    def _extract(self, segments, show_loading) -> ndarray:
        """
        Turn :param segments into a feature matrix of size (n_segments, feature_dim)
        """
        if isinstance(segments, pd.DataFrame):
            if show_loading:
                segment_list = tqdm(segments["text"])
            else:
                segment_list = segments["text"]
            return pd.DataFrame(
                [self._segment_extract(segment) for segment in segment_list],
                index=segments.index,
            )

        return np.array([self._segment_extract(segment) for segment in segments])

    @abstractmethod
    def _segment_extract(self, segment: str) -> List[float]:
        pass
