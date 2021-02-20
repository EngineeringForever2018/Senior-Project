import pickle

import spacy
import torch
from numpy import ndarray
from torch.nn import Embedding
from torch.nn.utils.rnn import pack_padded_sequence
from pkg_resources import resource_stream

from notebooks.feature_extractors.base_feature_extractor import BaseFeatureExtractor
from notebooks.nets._style_encoder import StyleEncoder, ParEncoder, SentenceEncoder

nlp = spacy.load('en_core_web_sm')


class BaweNeuralExtractor(BaseFeatureExtractor):
    def __init__(self):
        bawe_train_stats = pickle.load(resource_stream('notebooks', 'bawe_train_stats.p'))
        self._pos_vocab = bawe_train_stats['pos_vocab']
        self._embedding = Embedding(len(self._pos_vocab), 10, padding_idx=self._pos_vocab['<pad>'])
        self._embedding.load_state_dict(torch.load(resource_stream('notebooks', 'bawe_embedding_sd.pt')))
        sentence_encoder = SentenceEncoder(10, 10)
        par_encoder = ParEncoder(10, 5)
        self._style_encoder = StyleEncoder(sentence_encoder, par_encoder)
        self._style_encoder.load_state_dict(torch.load(resource_stream('notebooks.resources', 'bawe_style_encoder_sd.pt')))

    def extract(self, text: str) -> ndarray:
        doc = nlp(text)

        tokens = [[token.text for token in sent] for sent in doc.sents]
        pos_tokens = [[self._pos_vocab[token] for token in sent] for sent in tokens]

        max_sent_len = max([len(sent) for sent in pos_tokens])

        sent_tensors = []
        sent_lens = []
        for sent in pos_tokens:
            sent_tensor = torch.full([max_sent_len], self._pos_vocab['<pad>'])
            sent_len = torch.tensor(len(sent))
            sent_tensor[:sent_len] = torch.tensor(sent)

            sent_tensors.append(sent_tensor.unsqueeze(0))
            sent_lens.append(sent_len.unsqueeze(0))

        sent_count = len(sent_tensors)
        new_sent_count = sent_count - (sent_count % 4)

        tensor = torch.cat(sent_tensors, dim=0)[:new_sent_count]
        sent_lens = torch.cat(sent_lens, dim=0)[:new_sent_count]

        with torch.no_grad():
            embed_tensor = self._embedding(tensor)
            embed_tensor = torch.transpose(embed_tensor, 0, 1)
            packed_tensor = pack_padded_sequence(embed_tensor, sent_lens, enforce_sorted=False)
            features = self._style_encoder(packed_tensor)

        return features.numpy()


if __name__ == '__main__':
    extractor = BaweNeuralExtractor()

    print(extractor('Team 11-3 has established a charter to ensure that they are able to meet all deadlines and deliver on all requirements presented by the recommendation. Punctuality and professionalism are important to Team 11-3. As such, policies on deadlines, absences to meetings, and late arrivals have been determined. Deadlines for all major components of the project have been scheduled ahead of time. In the case that non-major, buffer deadlines are not met, the responsible engineer will have to write a formal apology to the rest of the team. If an engineer does not have all their required work for a major deadline, they will be reported to the ENGR 301 T.A.s. The engineers of Team 11-3 have agreed to weekly meetings on Wednesday. These may either be informal meetings where they simply report on their progress that week, or they may be formal meetings where plans for major components of the project are discussed. If a formal meeting is missed, the engineer responsible must bring coffee for everyone in the next meeting. Meetings will not be delayed waiting for late arrivals, so late members must be able to catch up on their own. Table 3 details these policies. With the team’s charter established, its culture can now be considered.'))
