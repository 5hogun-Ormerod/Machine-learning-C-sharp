# -*- coding: utf-8 -*-

import torch
from torch import nn

class TextToSeq(nn.Module):
    
    def __init__(self, tokenizer):
        super(TextToSeq, self).__init__():
        self.tokenizer = tokenizer


    def forward(self, texts):
        batch_size = len(texts)
        encodings = [tokenizer.encode(t) for t in texts]
                    
            