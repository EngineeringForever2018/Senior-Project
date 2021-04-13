from abc import ABC, abstractmethod
from typing import List, Union


class BaseProfile(ABC):
    @abstractmethod
    def feed(self, text: Union[str, List[str]]):
        pass

    @abstractmethod
    def score(self, text: Union[str, List[str]]) -> float:
        pass
