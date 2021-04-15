from notebooks.utils import split_into_sentences


class Sentencizer:
    def __call__(self, text: str):
        return list(split_into_sentences(text))
