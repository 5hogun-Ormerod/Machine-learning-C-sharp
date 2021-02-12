import torch
from torch import nn

class GELU(nn.Module):
    
    def forward(self, x):
        return x * torch.sigmoid(1.702 * x)