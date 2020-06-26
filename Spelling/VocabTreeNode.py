# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:36:56 2020

@author: Christopher Ormerod
"""

import sys
import numpy as np
from tqdm import tqdm


class VocabTreeNode():
    
    # This class is aimed at the most efficient manner to do spelling 
    # corrections. We have used optimized classes and structures to minimize
    # both memory and CPU power.
    
    def __init__(self, vocab = None):
        pass
    
    def build(self, vocab):
        assert isinstance(vocab, dict)
        for w, count in tqdm(vocab.items()):
            self.__insert(w, count)
       
    def __insert(self, word, count):
        assert isinstance(word, str)
        if word.isascii():
            node = self
            for letter in word:
                try:
                    if letter not in node.children:
                        node.children[letter] = VocabTreeNode()
                    node = node.children[letter]
                except:
                    node.children = {letter:VocabTreeNode()}
                    node = node.children[letter]
            node.count = count
            
    def weight(self):
        try:
            max_over_leaves = max([n.weight() for n in self.children.values()])
        except:
            max_over_leaves = 0
        
        try:
            self_weight = self.count
        except:
            self_weight = 0
        return max(max_over_leaves, self_weight)
                
    def __getitem__(self, word):
        node = self.search(word)
        if node is not None:
            try:
                return node.count
            except: 
                return 0
    
    def score(self, word):
        node = self.__search(word)
        return node.weight()
            
    def search(self, word):
        assert isinstance(word, str)
        if word.isascii():
            node = self
            for letter in word:
                try:
                    node = node.children[letter]
                except:
                    return None
            return node
        else:
            return None
        
    def next_letter(self, partial_word):
        node = self.search(partial_word)
        if node is not None:
            try:
                weights = {k:n.weight() for k,n in node.children.items()}
                sum_weights = sum(weights.values())
                return {k:w/sum_weights for k,w in weights.items()}
            except:
                return {}
        else:
            return {}
        
    def vocabRecursive(self, prefix):
        output = {}
        try:
            if self.count > 0:
                output[prefix] = self.count
        except:
            pass
        
        try:
            for c, node in self.children.items():
                new_words = node.vocabRecursive(prefix+c)
                output.update(new_words)
        except:
            pass
        return output
    
    def complete(self, word):
        node = self.search(word)
        if node is None:
            return {}
        else:
            return node.vocabRecursive(word)
    
    def vocab(self):
        return self.vocabRecursive("")
        
        