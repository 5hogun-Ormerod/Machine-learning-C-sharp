# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:08:48 2020

@author: Christopher Ormerod
"""

import editdistance as ed
    
def Edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def EditDistance(str1, str2):
    return ed.eval(str1,str2)

