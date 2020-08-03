# -*- coding: utf-8 -*-
"""
@author: Christopher Ormerod

This module is a base module for my spell-correction code. It serves the 
purpose of returning all elements in a vocabulary of a specified edit distance
in addition to returning the phonetic edit distance. The code is based
on a Tree structure that 
"""

import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from Utils import tokenize
from Spelling import phonetic_distance

class VocabTreeNode():
    
    # This class is aimed at the most efficient manner to do spelling 
    # corrections. We have used optimized classes and structures to minimize
    # both memory and required CPU power.
    
    def __init__(self, vocab = None):
        """
        Parameters
        ----------
        vocab : Dict
            We want a set, dictionary or counter. If vocab is specified, 
            the structure is built on the vocab.
        """
        self.char = ""
        self.parent = None
        if vocab is not None:
            self.build(vocab)
            
    def build(self, vocab):
        """
        Parameters
        ----------
        vocab : set or dict/counter
            This is a set of words or dict of ints with frequency information.
            if the structure passed is a set, then the set of words is pass
            with a default count of 1.
        """
        assert isinstance(vocab, dict) or isinstance(vocab,set)
        if isinstance(vocab,set):
            vocab = {w:1 for w in vocab}
        for w, count in tqdm(vocab.items()):
            self.__insert(w, count)
       
    def __insert(self, word, count):
        """
        Parameters
        ----------
        word : str
            This adds a word to the dictionary.
        count : int
            In addition to adding the word, we add frequency information.
        """
        assert isinstance(word, str) and isinstance(count,int)
        if word.isascii():
            node = self
            for letter in word:
                try:
                    if letter not in node.children:
                        node.children[letter] = VocabTreeNode()
                        node.children[letter].char = letter
                        node.children[letter].parent = node
                    
                    node = node.children[letter]
                except:
                    node.children = {letter:VocabTreeNode()}
                    node.children[letter].char = letter
                    node.children[letter].parent = node
                    
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
                
    def __getitem__(self, w):
        node = self.search(w)
        if node is not None:
            try:
                return node.count
            except: 
                return 0
    
    def score(self, word):
        node = self.__search(word)
        return node.weight()
            
    def search(self, word):
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
        
    def word(self):
        node = self
        w = ""
        while node.parent is not None:
            w = node.char + w
            node = node.parent
        return w
        
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
    
    def candidates(self, word, maxCost):
        currentRow = range( len(word) + 1 )    
        results = []
        for letter in self.children:
            self.searchRecursive(self.children[letter], letter, 
                                 word, currentRow, results, 
                                 maxCost)
        res_dict = {}
            
        for token, cost in results:
            if token in res_dict:
                if cost < res_dict[token]['edit_distance']:
                    res_dict[token]['edit_distance'] = cost
            else:
                res_dict[token] = {'edit_distance':cost,
                                   'phonetic_distance':phonetic_distance(token,word)}
        return res_dict
            
    def searchRecursive(self, node, letter, word, previousRow, 
                        results, maxCost):
        columns = len( word ) + 1
        currentRow = [ previousRow[0] + 1 ]
        for column in range( 1, columns ):
            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1
            if word[column - 1] != letter:
                replaceCost = previousRow[ column - 1 ] + 1
            else:                
                replaceCost = previousRow[ column - 1 ]
            currentRow.append( min( insertCost, deleteCost, replaceCost ) )
        try:
            if currentRow[-1] <= maxCost and node.word != None:
                results.append( (node.word, currentRow[-1] ) )
        except:
            pass
        if min( currentRow ) <= maxCost:
            try:
                for next_letter in node.children:
                    self.searchRecursive( node.children[next_letter], next_letter, word,
                                          currentRow, results, maxCost)
            except:
                pass
