from abc import ABC, abstractmethod

from numpy import ndarray


class BaseFeatureExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> ndarray:
        """
        Extract features from the given text.

        :param text: The text to extract features from.

        :return: The feature vectors as a numpy array of size (batch_size, feature_dim). For example, if this feature
        extractor extracts a feature vector of size 10 for every paragraph in the text, and there are 20 paragraphs in
        the text, the returned array will have size (20, 10).
        """
        pass

    def __call__(self, text: str) -> ndarray:
        return self.extract(text)
