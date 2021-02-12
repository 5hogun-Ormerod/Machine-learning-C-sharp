# -*- coding: utf-8 -*-
import ujson
import threading 
import concurrent.futures
from Spelling import phonetic_representation, EditDistance
from collections import Counter
from tqdm import tqdm
import heapq
import numpy as np

phonemes = '0AFHJKLMNPRSTX'

def edits1(rep):
    """
    Parameters
    ----------
    rep : str
        A phonetic representation of a given word.

    Returns
    -------
    Set
        The set of all phonetic representations of edit distnace 1 from a
        target representation.

    """
    splits     = [(rep[:i], rep[i:])    for i in range(1,len(rep) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in phonemes]
    inserts    = [L + c + R               for L, R in splits for c in phonemes]
    return set(deletes + transposes + replaces + inserts)


class phonetic_node:
    
    def __init__(self):
        self.words = set()
        self.children = dict()
    
class phonetic_tree:
    
    def __init__(self, words: Counter):
        self.root = phonetic_node()
        self.vocab = dict()
        self.inverse_vocab = dict()
        self.build(words)
        self.counter = words
        
    def build(self, words):
        for w in tqdm(words):
            self.insert(w)
        
    def insert(self,word):
        phonemes = phonetic_representation(word)
        self.vocab[word] = phonemes
        for rep in  phonemes:
            if rep not in self.inverse_vocab:
                self.inverse_vocab[rep] = {word}
            else:
                self.inverse_vocab[rep].add(word)
            
            n = self.root
            for phoneme in rep:
                if phoneme not in n.children:
                    n.children[phoneme] = phonetic_node()
                n = n.children[phoneme]
            n.words.add(word)
        
    def ultra_fast_search(self,
                          word,
                          representations,
                          results):
        out = set()
        for p in representations:
            if p in self.inverse_vocab:
                out = out.union(self.inverse_vocab[p])
        return out
    
    def fast_search(self,
                   word,
                   representations,
                   results):
        dist1 = set()
        for p in  [p for p in representations if p != ""]:
            dist1 = dist1.union(edits1(p))
        out = set()
        for p in dist1:
            if p in self.inverse_vocab:
                out = out.union(self.inverse_vocab[p])
        return out
            
    
    def search(self, 
               word, 
               maxcost = None, 
               topn=10):
        key = lambda x:np.log(self.counter[x]+2) - 200*EditDistance(word,x)
        results = set()
        if word in self.vocab:
            representations = self.vocab[word]
        else:
            representations = phonetic_representation(word)
        if maxcost is None:
            check = self.ultra_fast_search(word,representations,results)
            if len(check) < topn:
                check = self.fast_search(word,representations,results)
            if len(check) < topn:
                check = self.slow_search(word,representations,results)
            if len(check) < topn:
                check.extend(self.check_bi_phonics(word))
            if len(check) > 0:
                return heapq.nlargest(topn, 
                                      check, 
                                      key=key)
            else:
                print("NFI what {} is".format(word))
                return [word]
        else:
            if maxcost == 0:
                results = self.ultra_fast_search(word,representations,results)
            elif maxcost == 1:
                results = self.fast_search(word,representations,results)
            else:
                results = self.slow_search(word,representations,results,maxcost=maxcost)
            if len(results) < topn:
                results.extend(self.check_bi_phonics(word))
            
            if len(results) > 0:
            
                return heapq.nsmallest(topn, 
                                       list(set(results)), 
                                       key=key)
            else:
                print("NFI what {} is".format(word))
                return [word]

    def slow_search(self,
                   word,
                   representations,
                   results,
                   maxcost=2):
        """
        Parameters
        ----------
        word : str
            The misspelled word to look up
        representations : str
            A phonetic representation of the word.
        results : List
            A list to append the results to.
        maxcost: int
            This tells us to what phonetic edit distance we wish to search. 
        
        Returns
        -------
        results : List
            A list containing all elements of the results parameter in
            addition to all elements with one phonetic representation that
            is the same to with an edit distance of 2. This 
        """
        
        for rep in representations:
            if rep != "":
                currentRow = range( len(rep) + 1 )
            
                self.searchRecursive(self.root.children[rep[0]], 
                                     rep[0], 
                                     rep, 
                                     currentRow, 
                                     results, 
                                     maxCost=maxcost)
        return results
                
        
    def searchRecursive(self, 
                        node, 
                        ph, 
                        rep, 
                        previousRow, 
                        results, 
                        maxCost):
        columns = len( rep ) + 1
        currentRow = [ previousRow[0] + 1 ]
    
        for column in range( 1, columns ):

            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1
    
            if rep[column - 1] != ph:
                replaceCost = previousRow[ column - 1 ] + 1
            else:                
                replaceCost = previousRow[ column - 1 ]    
            currentRow.append( min( insertCost, deleteCost, replaceCost ) )

        if currentRow[-1] <= maxCost and len(node.words) > 0:
            results = results.union(node.words)
    
        if min( currentRow ) <= maxCost:
            for next_letter in node.children:
                self.searchRecursive(node.children[next_letter], 
                                     next_letter, 
                                     rep, 
                                     currentRow, 
                                     results, 
                                     maxCost)
                


