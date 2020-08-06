# -*- coding: utf-8 -*-

from abc import ABC

class SequenceToSequenceEngine(ABC):

    def __init__(self):
        pass
    
    def save(self, path):
        raise NotImplemented
                
    def convert(self, text):
        raise NotImplemented
        
    def fit(self, s2s_dataset):
        raise NotImplementedError
        
        
class SequenceToSequenceEngine(ABC):
    
    def __init__(self):
        pass
    
    def save(self, path):
        raise NotImplemented
                
    def predict(self, text):
        raise NotImplemented
        
    def fit(self, class_dataset):
        raise NotImplementedError
        
    
class LanguageModelEngine(ABC):
    
    def __init__(self):
        pass
    
    def save(self, path):
        raise NotImplemented
                
    def generate(self, text):
        raise NotImplemented
        
    def fit(self, text_dataset):
        raise NotImplementedError