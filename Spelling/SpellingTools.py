# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:16:24 2020

@author: Christopher Ormerod
"""
from collections import Counter

def count_vocab(textset, 
                tokenizer):
    TokSet = tokenizer.tokenize_set(textset)
    
    for out in TokSet:
        tokens = out['tokens']
        for w in tokens:
            