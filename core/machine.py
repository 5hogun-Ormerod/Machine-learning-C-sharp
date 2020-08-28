# -*- coding: utf-8 -*-

from abc import ABC

class SequenceToSequenceEngine(ABC):

    def __init__(self):
        pass
    
    def save(self, path):
        raise NotImplemented
                
    def convert(self, text):
        raise NotImplemented
        
    def fit(self, dataset, text_col, score_col):
        raise NotImplementedError
    
        
        
class SequenceToLabelEngine(ABC):
    
    def __init__(self):
        pass
    
    def save(self, path):
        raise NotImplemented
                
    def predict(self, text):
        raise NotImplemented
        
    def fit(self, class_dataset):
        raise NotImplementedError
        
        
