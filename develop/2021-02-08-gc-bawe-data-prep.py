#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pickle
from pathlib import Path
from os.path import join
from tqdm import tqdm
import torch


# In[9]:


txt_corpus_path = Path('../data/bawe/CORPUS_TXT')


# Reserve 20% of the essays for a testing set.

# In[ ]:


from pathlib import Path


# In[ ]:


from os import listdir
from os.path import isfile, join

dir_contents = listdir(txt_corpus_path)


# In[ ]:


dir_contents[:5]


# In[ ]:


only_files = [f for f in dir_contents if isfile(join(txt_corpus_path, f))]


# In[ ]:


only_files[:5]


# In[ ]:


import random

random.seed(0)

random.shuffle(only_files)


# In[ ]:


only_files[:5]


# In[ ]:


len(only_files) / 20


# In[ ]:


training_files = only_files[:-184]
testing_files = only_files[-184:]


# In[ ]:


training_files[-5:]
testing_files[:5]


# In[ ]:


import pickle

pickle.dump({'train': training_files, 'test': testing_files}, open(Path('../data/bawe_splits.p'), 'wb'))


# In[2]:


import spacy

nlp = spacy.load('en_core_web_sm')


# In[ ]:


doc = nlp('When I was a boy, I fell down. Then I got back up.')


# In[ ]:


sents = [sent for sent in doc.sents]


# In[ ]:


type(sents[0])


# In[ ]:


pos = [[token.pos_ for token in sent] for sent in sents]


# In[ ]:


pos


# In[ ]:


import torch


# In[ ]:


from torch.nn import Embedding


# In[ ]:


embedding = Embedding(7, 5, padding_idx=1)


# In[ ]:


embedding(torch.tensor([1]))


# In[3]:


def find_max_sent_len(pos_text, nlp_=nlp):
    sent_lens = [len(sent) for sent in pos_text]
    
    return max(sent_lens)

def find_pos_set(pos_text, nlp_=nlp):
    sets = [set(sent) for sent in pos_text]
    
    result = set()
    
    for set_ in sets:
        result |= set_
    
    return result

def pos_tag(text, nlp_=nlp):
    sents = [sent for sent in nlp_(text).sents]
    
    return [[token.pos_ for token in sent] for sent in sents]

def pos_tag_file(f, nlp_=nlp):
    text = open(join(txt_corpus_path, Path(f))).read()
    
    return pos_tag(text)


# In[4]:


splits = pickle.load(open(Path('../data/bawe_splits.p'), 'rb'))


# In[5]:


training_files = splits['train']


# In[9]:


max_sent_lens = []
pos_set = set()
for f in tqdm(training_files):
    text = open(join(txt_corpus_path, Path(f))).read()
    
    pos_text = pos_tag(text)
    
    max_sent_lens.append(find_max_sent_len(pos_text))
    pos_set |= find_pos_set(pos_text)

max_sent_len = max(max_sent_lens)


# In[13]:


max_sent_len


# In[16]:


pos_counts = 


# In[17]:


from collections import Counter


# In[20]:


from torchtext.vocab import Vocab


# In[23]:


pos_vocab = Vocab(Counter(pos_set))


# In[27]:


pos_vocab['asf']


# In[28]:


pickle.dump({'max_sent_len': max_sent_len, 'pos_vocab': pos_vocab}, open('../data/bawe_train_stats.p', 'wb'))


# In[6]:


bawe_train_stats = pickle.load(open('../data/bawe_train_stats.p', 'rb'))
max_sent_len = bawe_train_stats['max_sent_len']
pos_vocab = bawe_train_stats['pos_vocab']


# In[37]:


pos_vocab['<pad>']


# In[7]:


def to_tensor(pos_text, par_len=4, max_sent_len_=max_sent_len):
    sent_tensors = []
    sent_lens = []
    
    for sent in pos_text:
        sent_tensor, sent_len = sent_to_tensor(sent, max_sent_len_)
        
        sent_tensors.append(sent_tensor.unsqueeze(0))
        sent_lens.append(sent_len)
    
    sent_count = len(sent_tensors)
    new_sent_count = sent_count - (sent_count % par_len)
    
    tensor = torch.cat(sent_tensors, dim=0)[:new_sent_count]
    lens = torch.cat(sent_lens, dim=0)[:new_sent_count]
    
    tensor = torch.reshape(tensor, [-1, 4, max_sent_len_])
    lens = torch.reshape(lens, [-1, 4])
    
    return tensor, lens

def sent_to_tensor(sent, max_sent_len_=max_sent_len, pos_vocab_=pos_vocab):
    pos_indices = [pos_vocab_[pos] for pos in sent]
    sent_len = len(pos_indices)
    
    tensor = torch.full([max_sent_len_], pos_vocab_['<pad>'])
    
    non_padded = torch.tensor(pos_indices)
    
    tensor[:sent_len] = non_padded
    
    return tensor, torch.tensor([sent_len])


# In[8]:


pos_text = pos_tag_file(training_files[0])

to_tensor(pos_text)[0].size()


# In[14]:



        tensor = torch.reshape(tensor, [-1, 4, max_sent_len])
        sent_lens = torch.reshape(sent_lens, [-1, 4])labels_tensors = []

for f in tqdm(training_files):
    pos_text = pos_tag_file(f)
    
    tensor, sent_lens = to_tensor(pos_text, 4, max_sent_len)
    
    label = int(f[:4])
    
    labels_tensors.append((label, tensor, sent_lens))


# In[ ]:


labels_tensors[0]


# In[16]:


labels_tensors.sort(key=lambda label_tensor: label_tensor[0])


# In[22]:


labels_tensors[0][2]


# In[24]:


new_labels_tensors = [(torch.full([len(sent_lens)], label), tensor, sent_lens) for label, tensor, sent_lens in labels_tensors]


# In[26]:


labels_list, tensor_list, sent_lens_list = zip(*new_labels_tensors)


# In[27]:


labels_list[0]


# In[32]:


labels = torch.cat(labels_list, dim=0).contiguous()
tensor = torch.cat(tensor_list, dim=0).contiguous()
sent_lens = torch.cat(sent_lens_list, dim=0).contiguous()


# In[33]:


sent_lens[:5]


# In[35]:


torch.save(labels, '../data/bawe-preprocess/labels.pt')
torch.save(tensor, '../data/bawe-preprocess/data.pt')
torch.save(sent_lens, '../data/bawe-preprocess/sent_lens.pt')


# In[40]:


len(labels)


# In[45]:


label_set = set([int(label) for label in labels])


# In[48]:


sum(labels == 1)


# In[ ]:


label_counts = {int(label): sum(labels == label) for label in tqdm(label_set)}


# In[ ]:





# In[58]:


label_set_list = list(label_set)
label_set_list.sort()

position = 0
label_starts = {}
for label in label_set_list:
    label_starts[label] = position
    position += int(label_counts[label])


# In[59]:


label_ends = {label: label_starts[label] + int(label_counts[label]) for label in label_counts}


# In[65]:


min(label_counts.values())


# In[64]:


label_ends[6998]


# In[66]:


pickle.dump({'label_counts': label_counts, 'label_starts': label_starts, 'label_ends': label_ends}, open('../data/bawe-preprocess/label_stats.p', 'wb'))


# In[41]:


22 - (22 % 4)

