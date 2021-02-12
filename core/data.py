# -*- coding: utf-8 
from torch.utils.data import Dataset
import pandas as pd
import os
from collections.abc import Iterable
from Utils import Fast_File
from tqdm import tqdm
from collections import deque

class TextSet(Dataset):
    
    def __init__(self, 
                 text_series,
                 status_bar = False):
        if isinstance(text_series, str):
            self.text_series = pd.Series([text_series])
        elif isinstance(text_series, pd.Series):
            self.text_series = text_series
        elif isinstance(text_series, Iterable):
            if isinstance(texts, Fast_File):
                self = FastFileTextSet(texts)
            else:
                self.text_series = pd.Series(list(text_series))
        self.idx = 0
        self.status_bar = status_bar
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.idx == 0:
            self.qbar = tqdm(range(len(self)))
        if self.idx < len(self):
            text = self.__getitem__(self.idx)
            self.idx += 1
            if self.status_bar == True:
                self.qbar.update()
            return text
        else:
            self.reset()
            raise StopIteration
    
    def reset(self):
        self.idx = 0
    
    def __add__(self, texts):
        self.reset()
        if isinstance(texts, str):
            return self.__add__([texts])
        elif isinstance(texts, pd.Series):
            return TextSet(pd.concat([self.text_series, texts], ignore_index=True))
        elif isinstance(texts, TextSet):
            return self.__add__(texts.text_series)
        elif isinstance(texts, Iterable):
            if isinstance(texts, Fast_File):
                return FastFileTextSet(texts)
            else:
                return self.__add__(pd.Series(list(texts)))
        else:
            raise "Unsupported Type"
    
    def __getitem__(self, idx):
        text = str(self.text_series.iloc[idx])
        return {"text":text}
        
    def __len__(self):
        return len(self.text_series)

class TokenizedSet(TextSet):

    def __init__(self, 
                 text_series,
                 tokenizer):
        super().__init__(text_series)
        self.tokenizer = tokenizer
        
    def __getitem__(self, idx):
        output = TextSet.__getitem__(self,idx)
        tokens = self.tokenizer.tokenize(output['text'])
        output.update({"tokens":tokens})
        return output
    
    def __add__(self,texts):
        TS = TextSet.__add__(self, texts)
        return TokenizedSet(TS.text_series,
                            self.tokenizer)
    
class TupleSet(TokenizedSet):
    
    def __init__(self, 
                 text_series, 
                 tokenizer,
                 n):
        super().__init__(text_series,tokenizer)
        self.n = n
        self.number_of_texts = len(self.text_series)
        self.set_text(0)
        
    def __iter__(self):
        return self
    
    def set_text(self, text_index):
        self.text_idx = text_index
        self.idx = 0
        self.current_tokens = self.tokenizer.tokenize(self.text_series.iloc[self.text_idx])
        self.current_length = len(self.current_tokens)
        self.bag = deque(maxlen=self.n)
        
    def __next__(self):
        if self.idx > self.current_length-1:
            if self.text_idx +1 >= self.number_of_texts: 
                self.set_text(0)
                raise StopIteration
            else:
                self.set_text(self.text_idx+1)
                return self.bag
        else:
            self.bag.append(self.current_tokens[self.idx])
            self.idx+=1
            return self.bag
        
    def __add__(self,texts):
        TS = TokenizedSet.__add__(self, texts)
        return TupleSet(TS.text_series,
                        self.tokenizer,
                        self.n)

class FastFileTextSet(TextSet):

    def __init__(self, FF):
        self.text_series = [FF]
        
        
    def __add__(self, FF):
        assert isinstance(FF, (FastFileTextSet, Fast_File))
        