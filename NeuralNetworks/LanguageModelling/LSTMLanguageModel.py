import torch
from NeuralNetworks.core import SequenceToSequenceEngine
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence



class LSTMmodel(nn.Module):
    
    def __init__(self, units, layers, input_dimension):
        super(LSTMmodel, self).__init__()
        self.blocks = nn.ModuleList()
        self.units = units
        self.layers = layers
        self.input_dimension = input_dimension
        
        for _ in range(layers):
            self.blocks.append(block(dim))
        
    class block(nn.Module):
        
        def __init__(self):
            super(block, self).__init__()
            self.lstm = nn.LSTM(input_size = self.input_dimension,
                                hidden_size = self.units,
                                num_layers = self.layers,
                                batch_first = True)
            
        def forward(self, X):
            pass
            
        



class LSTMSeq2Seq(SequenceToSequenceEngine):
    
    def __init__(self, units, layers)
        
        
        
        
        

            
    