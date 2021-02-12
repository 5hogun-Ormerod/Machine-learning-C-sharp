# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 10:08:48 2020

@author: Christopher Ormerod
"""

import editdistance as ed
    
def EditDistance(str1, str2):
    return ed.eval(str1,str2)

