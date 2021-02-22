import os
from os.path import join

import spacy


class POSVocab:
    pass


def split_text(text: str, sentences_per_split, nlp=None):
    nlp = nlp or default_nlp()
    doc = nlp(text)

    splits = []
    split = ""
    count = 0
    for sentence in doc.sents:
        if count == sentences_per_split:
            splits.append(split)
            count = 0
            split = ""

        split += sentence.text
        count += 1

    return splits


def default_nlp():
    return spacy.load('en_core_web_sm')


def split_into_sentences(text: str, nlp=None):
    nlp = nlp or default_nlp()

    doc = nlp(text)

    for sentence in doc.sents:
        yield sentence.text


def init_data_dir(project_path):
    data_dir = join(project_path, 'data')
    raw_dir = join(data_dir, 'raw')
    preprocess_dir = join(data_dir, 'preprocess')

    # Data directory must come first!
    dirs = [data_dir, raw_dir, preprocess_dir]
    for dir_ in dirs:
        if not os.path.isdir(dir_):
            os.mkdir(dir_)


def tokenize(sentence: str, nlp=None):
    nlp = nlp or default_nlp()

    return [str(token.pos_) for token in nlp(sentence)]


def pos_tag(sentence: list, pos_vocab=None):
    pos_vocab = pos_vocab or POSVocab()

    return [pos_vocab[token] for token in sentence]
