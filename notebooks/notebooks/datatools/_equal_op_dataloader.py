from os.path import join
from pathlib import Path

import torch
from torch.nn.utils.rnn import pack_padded_sequence
from torch.utils.data import TensorDataset


class EqualOpDataLoader:
    def __init__(self, dataset, bs=1, pipeline=None):
        self.dataset = dataset
        self.bs = bs
        self.collate_fn = pipeline or (lambda x: x)

        authors, _, _, _ = zip(*self.dataset.df.index.tolist())

        self.label_set = torch.tensor(sorted(list(set(authors))))

        # _, _, self.labels = dataset[:]
        # self.label_set = torch.tensor(sorted(list(set([int(label) for label in self.labels]))))
        self.batch_count = int(len(dataset.df) / bs)

    def __iter__(self):
        bs = self.bs

        # Iterating for this long will ensure that most of the dataset is covered.
        for _ in range(self.batch_count):
            # Choose two sets of random labels for this batch.
            order = torch.randperm(len(self.label_set))
            batch_labels = self.label_set[order[:bs]]
            different_labels = self.label_set[order[bs:2 * bs]]

            # The first labels will simply be the labels from the batch. ~50% of the second labels will be the same as
            # the first labels and ~50% will be different.
            first_labels = batch_labels
            second_labels = torch.clone(batch_labels)

            # Create a boolean index list where ~50% of the values are True. Use this to decide which labels will be
            # different.
            different_selection = torch.bernoulli(torch.full([bs], 0.5)).to(bool)
            second_labels[different_selection] = different_labels[different_selection]

            first_labels, _ = torch.sort(first_labels)
            second_labels, _ = torch.sort(second_labels)
            first_df = self.dataset.sample_authors(first_labels.tolist())
            second_df = self.dataset.sample_authors(second_labels.tolist())

            yield self.collate_fn(first_df), self.collate_fn(second_df)

            # first_data, first_sent_lens, first_labels = self._sample_data(first_labels)
            # second_data, second_sent_lens, second_labels = self._sample_data(second_labels)

            # yield self.collate_fn((first_data, first_sent_lens, first_labels),
            #                       (second_data, second_sent_lens, second_labels))

    def _sample_data(self, chosen_labels):
        """Get random data points for every label in :param chosen_labels"""
        result = [self._sample_point(label) for label in chosen_labels]

        data, sentence_lengths, labels = zip(*result)

        data = torch.cat(data, dim=0)
        sentence_lengths = torch.cat(sentence_lengths, dim=0)
        labels = torch.cat(labels, dim=0)

        return data, sentence_lengths, labels

    def _sample_point(self, label):
        """Get a random point from the dataset for :param label"""
        # If self.labels[i] == label, then we can get dataset[i] in order to get data for label.
        selection = (self.labels == label)
        dataset_selection = self.dataset[selection]

        data, sentence_lengths, chosen_label_cloned = dataset_selection

        selected_index = torch.randint(high=len(chosen_label_cloned), size=(1,))
        # Use slice so that returned items are list instead of objects.
        selected_slice = slice(selected_index, selected_index+1)

        return data[selected_slice], sentence_lengths[selected_slice], chosen_label_cloned[selected_slice]

    def __len__(self):
        return self.batch_count


class Preprocessor:
    def __init__(self, dev):
        self.dev = dev

    def __call__(self, first, second):
        first, second = self._pack(first, second)

        return self._move(first, second)

    @staticmethod
    def _pack(first, second):
        first_data, first_sentence_lengths, first_labels = first
        second_data, second_sentence_lengths, second_labels = second

        def reform(data, sentence_lengths):
            """Flatten paragraphs and then transpose into (seq_len, 4 * batch_size)"""
            batch_size, _, seq_len = data.size()

            # (4 * batch_size, seq_len, embedding_dim)
            reshaped = torch.reshape(data, [-1, seq_len])

            return torch.transpose(reshaped, 0, 1), torch.reshape(sentence_lengths, [-1])

        first_data, first_sentence_lengths = reform(first_data, first_sentence_lengths)
        second_data, second_sentence_lengths = reform(second_data, second_sentence_lengths)

        first_data = pack_padded_sequence(first_data, first_sentence_lengths, enforce_sorted=False)
        second_data = pack_padded_sequence(second_data, second_sentence_lengths, enforce_sorted=False)

        return (first_data, first_labels), (second_data, second_labels)

    def _move(self, first, second):
        first_data, first_labels = first
        second_data, second_labels = second

        return (first_data.to(self.dev), first_labels.to(self.dev)), \
               (second_data.to(self.dev), second_labels.to(self.dev))


# Entry point for debugging
if __name__ == '__main__':
    preprocessed_data_dir = Path('../../data/preprocess')
    resources_dir = Path('../../resources')

    train_data = torch.load(join(preprocessed_data_dir, 'bawe_train_data.pt'))
    train_sentence_lengths = torch.load(join(preprocessed_data_dir,
                                             'bawe_train_sentence_lengths.pt'))
    train_labels = torch.load(join(preprocessed_data_dir, 'bawe_train_labels.pt'))

    valid_data = torch.load(join(preprocessed_data_dir, 'bawe_valid_data.pt'))
    valid_sentence_lengths = torch.load(join(preprocessed_data_dir,
                                             'bawe_valid_sentence_lengths.pt'))
    valid_labels = torch.load(join(preprocessed_data_dir, 'bawe_valid_labels.pt'))

    train_set = TensorDataset(train_data, train_sentence_lengths, train_labels)
    valid_set = TensorDataset(valid_data, valid_sentence_lengths, valid_labels)

    valid_dl = EqualOpDataLoader(valid_set, bs=64, pipeline=Preprocessor(torch.device(0)))

    for (x1b, y1b), (x2b, y2b) in valid_dl:
        pass
