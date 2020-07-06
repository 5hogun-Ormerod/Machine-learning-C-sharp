# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:16:24 2020

@author: Christopher Ormerod
"""

from Spelling.PhoneticTools import phonetic_errors 
import random
from numpy.random import choice

from Utils import tokenize, detokenize



vowel_confusion = {'a':{'e':0.4,'i':0.3,'o':0.1,'u':0.1,'':0.1},
                   'e':{'a':0.2,'i':0.5,'o':0.1,'u':0.1,'':0.1},
                   'i':{'a':0.2,'e':0.4,'o':0.1,'u':0.1,'':0.1,'y':0.1},
                   'o':{'a':0.1,'e':0.1,'i':0.1,'u':0.6,'':0.1},
                   'u':{'a':0.1,'e':0.1,'i':0.1,'o':0.6,'':0.1},
                   'y':{'i':0.5,'y':0.5}}


consonant_confusion = {'c':{'s':0.2, 'c':0.6, 'cc':0.2},
                       'l':{'r':0.2, 'll':0.5,'w':0.3},
                       's':{'c':0.5, 'ss':0.2,'s':0.3},
                       'm':{'n':0.2, 'mm':0.2,'m':0.6},
                       'n':{'m':0.3,'nn':0.4,'n':0.3},
                       'r':{'w':0.2,'l':0.4, 'rr':0.4},
                       'w':{'r':0.6,'l':0.4},
                       't':{'d':0.4,'t':0.3,'tt':0.3}}



misspelling_config = {'phonetic':0.03,
                      'vowel':0.07,
                      'consonant':0.03,
                      'doubling':0.02,
                      'concatenation':0.02}

doubles = 'cmnsprt'

def random_misspelling(text):
    text = text.lower()
    tokens = tokenize(text)
    tokens = __random_phonetic_error(tokens)
    new_tokens = []
    for word in tokens:
        if random.random() < misspelling_config['phonetic']:
            if len(new_tokens) > 0:
                new_tokens[-1] = new_tokens[-1]+word
            else:
                new_tokens = [word]
        else:
            new_tokens.append(word)
    return detokenize(tokens)


def __random_phonetic_error(tokens):
    for i, word in enumerate(tokens):
        if word in phonetic_errors:
            if random.random() < misspelling_config['phonetic']:
                choices = phonetic_errors[word]
                new_word = random.choice(choices)
            else:
                new_word = word
        else:
            new_word = word
        
        newer_word = ""
        for letter in word:
            if letter in vowel_confusion:
                if random.random() < misspelling_config['vowel']:
                    newer_word += choice(list(vowel_confusion[letter].keys()),
                                       1, p = list(vowel_confusion[letter].values()))[0]
                else:
                    newer_word += letter
            elif letter in consonant_confusion:
                if random.random() < misspelling_config['consonant']:
                    newer_word += choice(list(consonant_confusion[letter].keys()),
                                       1, p = list(consonant_confusion[letter].values()))[0]
                else:
                    newer_word += letter
            else:
                newer_word += letter        
        
        for c in doubles:
            if c+c in newer_word:
                if random.random() < misspelling_config['doubling']:
                    newer_word = newer_word.replace(c+c,c)
        tokens[i] = newer_word
        
    return tokens
    