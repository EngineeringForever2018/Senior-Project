from tqdm import tqdm

from notebooks.utils import default_nlp


class POSSentenceTokenizer:
    def __init__(self, nlp=None):
        self.nlp = nlp or default_nlp()

    def tokenize_list(self, sentences: str, show_loading=False):
        if show_loading:
            sentence_iter = tqdm(sentences)
        else:
            sentence_iter = sentences

        token_matrix = [[token.pos_ for token in self.nlp(sentence)] for sentence in sentence_iter]

        return token_matrix

    def tokenize(self, text: str, show_loading=False):
        if show_loading:
            print('NLP...', flush=True)
        doc = self.nlp(text)
        if show_loading:
            print('NLP done.', flush=True)

        if show_loading:
            sent_iter = tqdm(doc.sents)
        else:
            sent_iter = doc.sents

        token_matrix = [[token.pos_ for token in sentence] for sentence in sent_iter]

        return token_matrix

    def __call__(self, *args, **kwargs):
        return self.tokenize(*args, **kwargs)

