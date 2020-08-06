# -*- coding: utf-8 -*-

from abc import ABC

class tokenizer(ABC):
    
    def __init__(self):
        pass
    
    def tokenize(self, text):
        raise NotImplementedError
        
    def detokenize(self, iterable):
        raise NotImplementedError
        
    def encode(self, text):
        raise NotImplementedError
        
    def decode(self, iterable):
        raise NotImplementedError