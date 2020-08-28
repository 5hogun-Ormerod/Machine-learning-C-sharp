# -*- coding: utf-8 -*-

import torch
from torch import nn
import warnings 
import numpy as np
from typing import Dict

def step_module(model : nn.Module,
                model_args : Dict[str, np.array],
                target : np.array,
                optimizer = None,
                critereon = nn.CrossEntropyLoss(),
                GPU = False):
    if not torch.cuda.is_available():
        if GPU == True:
            warnings.warn("CUDA not available, using CPU")
            GPU = False
    else:
        if GPU = True:
            model.cuda()
        else:
            model.cpu()
    
    optimizer.zero_grad()
    
    tensors = {k:torch.tensor(X) for k, X in model_args.items()}
    y = torch.tensor(target)
    
    if GPU == True:
        for k in tensors:
            tensors[k] = tensors[k].cuda()
        preds = model.forward(*tensors)
        y = y.cuda()
        
    preds = model.forward(X)
    loss = critereon(preds, y)
    loss.backward()
    optimizer.step()
    
    if GPU == True:
        
        
    