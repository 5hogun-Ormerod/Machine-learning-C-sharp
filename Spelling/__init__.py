# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:41:15 2020

@author: Christopher Ormerod
"""

from .Dictionary import word_counter
from .edit_distance_tools import EditDistance
from .PhoneticTools import phonetic_representation
from .PhoneticTree import phonetic_tree

PhoneticTree = phonetic_tree(word_counter)


