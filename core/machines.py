# -*- coding: utf-8 -*-

from abc import ABC

class Classifier(ABC):
    
    def __init__(self):
        raise NotImplementedError
        
    def predict(self, text):
        raise NotImplementedError
        
    def output(self, text):
        raise NotImplementedError
        
    def save(self, path):
        raise NotImplementedError
    
    def load(self, path):
        raise NotImplementedError
        
class TrainableClassifier(Classifier):
    
    def fit(self, 
            train_set,
            test_set):
        raise NotImplementedError
        