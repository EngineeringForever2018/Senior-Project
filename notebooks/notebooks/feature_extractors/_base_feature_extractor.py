from abc import ABC, abstractmethod
import pandas as pd


class BaseFeatureExtractor(ABC):
    def __call__(self, *args, **kwargs) -> pd.DataFrame:
        return self.extract(*args, **kwargs) 

    def extract(self, segments: pd.DataFrame, show_loading=False) -> pd.DataFrame:
        return self._extract(segments, show_loading)

    @abstractmethod
    def _extract(self, segments: pd.DataFrame, show_loading: bool) -> pd.DataFrame:
        pass
