# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:56:54 2021

@author: Christopher Ormerod
"""

import torch
from torch import nn

class LinearMeanHead(nn.Module):
    
    def __init__(self, 
                 in_features, 
                 max_scores):
        super(LinearMeanHead,self)__init__()
        self.max_scores = max_scores
        self.heads = nn.ModuleDict
        for k,v in self.max_scores.items():
            self.heads = nn.Linear(in_features = in_features,
                                   out_features=v + 1)            

    def forward(self,
                input_features)
        mean_features = torch.mean(input_features,1)
        return {k:self.heads[k](mean_features) for k in self.max_scores}
    

class LinearFirstHead(nn.Module):
    
    def __init__(self, 
                 in_features, 
                 max_scores):
        super(LinearFirstHead,self)__init__()
        self.max_scores = max_scores
        self.heads = nn.ModuleDict
        for k,v in self.max_scores.items():
            self.heads = nn.Linear(in_features = in_features,
                                   out_features=v + 1)            

    def forward(self,
                input_features)
        first_features = input_features[:,0,:]
        return {k:self.heads[k](first_features) for k in self.max_scores}