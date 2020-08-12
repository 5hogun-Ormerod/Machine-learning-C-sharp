# -*- coding: utf-8 -*-
from torch.utils.data import Dataset
from transformers.data.datasets import TextDataset
from copy import deepcopy
import torch

class DataSeriesSet(Dataset):
    
    def __init__(self, data):
        assert isinstance(data, pd.core.generic.NDFrame)
        self.__data = data
        
    def __repr__(self):
        desc = "Dataset(text, rows = {}".format(len(self))
        return desc
        
    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, index):
        return self.__data.iloc[i]


class DataFrameSet(DataSeriesSet):
        
    def __repr__(self):
        desc = "Dataset(columns = {"
        for k, c in enumerate(self.__data.columns):
            if k != 0 :
                desc = desc = ", "
            desc = desc + str(c)
        desc = desc + "}, rows = {}".format(len(self))
        return desc
        
    def __getitem__(self, index):
        return self.__data.iloc[i].to_dict()
    
    def column(self, label):
        return DataSeriesSet(self.__data[label])
    
class TensorTokenSet(Dataset):
    
    def __init__(self, dataset, tokenizer):
        self.dataset = dataset
        self.tokenizer = tokenizer
        
    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, index):
        item = self.dataset[index]
        if isinstance(item, dict):
            new_item = deepcopy(item)
            for key, value in new_item.items():
                if isinstance(value, str):
                    new_item[key] = torch.tensor(self.tokenizer.encode(value, 
                                                                       max_length = 1024,
                                                                       pad_to_max_length = True,
                                                                       truncation=True)).long()
        else:
            if isinstance(item, str):
                return torch.tensor(self.tokenizer.encode_plus(item, 
                                                               max_length = 1024,
                                                               pad_to_max_length = True,
                                                               truncation=True)['input_ids'])
                    