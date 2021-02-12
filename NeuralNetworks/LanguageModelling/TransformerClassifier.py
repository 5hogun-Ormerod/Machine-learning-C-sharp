from core.machines import TrainableClassifier
import pytorch_lightning as pl

class MachineWrapper(TrainableClassifier):
    
    def __init__(self, 
                 model,
                 targets):
        self.model = pretrained_type
        self.targets = targets
        
    def predict(self, text):
        
        
    def output(self, text):
        raise NotImplementedError
        
    def save(self, path):
        raise NotImplementedError
    
    def load(self, path):
        raise NotImplementedError
    