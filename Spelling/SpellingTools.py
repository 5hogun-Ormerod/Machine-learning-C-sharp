# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:16:24 2020

@author: Christopher Ormerod
"""

from VocabTreeNode import VocabTreeNode
from Dictionary import words

def count_vocab(dataset, tokenizer):
    vocab = dict()
    for data in dataset:
        tokens = tokenizer.tokenize(data)
        for token in tokens:
            vocab[token] = vocab[token] + 1
    return vocab