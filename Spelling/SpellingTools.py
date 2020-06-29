# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:16:24 2020

@author: Christopher Ormerod
"""

from Spelling.PhoneticTools import phonetic_errors 
import random

from Utils import tokenize

misspelling_config = {'phonetic':1.0,
                      'two-to-one':0.1,
                      'a-vs-e':0.1,
                      'c-vs-s':0.05,
                      'swap-o-u':0.1,
                      'swap-i-e':0.1,
                      'miss-vowel':0.01,
                      'aly-vs-ly':0.1,
                      'concatenation':0.02,}

def random_misspelling(text):
    tokens = tokenize(text)
    tokens = __random_phonetic_error(tokens)
    


def __random_phonetic_error(tokens):
    for i, word in tokens:
        if word in phonetic_errors:
            if random.random() < misspelling_config['phonetic']:
                choices = phonetic_errors[word]
                choices.remove[word]
                new_word = random.choice(choices)
                print("{} -> {}".format(word,new_word))
                tokens[i] = new_word
    return tokens
    