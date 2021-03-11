from notebooks.utils import default_nlp


class POSSentenceTokenizer:
    def __init__(self, nlp=None):
        self.nlp = nlp or default_nlp()

    def tokenize(self, text: str):
        doc = self.nlp(text)

        token_matrix = [[token.pos_ for token in sentence] for sentence in doc.sents]

        return token_matrix

    def __call__(self, *args, **kwargs):
        return self.tokenize(*args, **kwargs)

