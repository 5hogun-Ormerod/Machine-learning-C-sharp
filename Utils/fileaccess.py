# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:25:51 2020

@author: Christopher Ormerod
"""

import mmap
import os
from tqdm import tqdm
import numpy as np
from collections import deque
import random
from tqdm import tqdm
from torch.utils.data import Dataset

class Fast_File(Dataset):
    
    # This is a wrapper for the process of enumerating the endlines of a 
    # file, then accessing lines using the mmap function. This is essentially
    # a faster version of the linecache which is slightly faster than 
    # linecache while performing approximately the same function up to
    # conversion from bytes to string.
    
    def __init__(self, 
                 file = None,
                 shuffle = False,
                 status_bar = True,
                 string = True):
        
        self.shuffle = shuffle
        self.file = file
        self.status_bar = status_bar
        self.string = string
        
        if file is not None:
            self.cache(file)
        self.count = 0
    
    def __repr__(self):
        return "Dataset(schema: ('text':str ), path = {}, rows = {})".format(self.file,len(self))
            
    def __iter__(self):
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self,  arg_type, value, traceback):
        self.close()
    
    def __next__(self):
        if self.count == 0:
            self.qbar = tqdm(range(len(self)))
        if self.count < len(self):
            text = self.getline(self.order[self.count])
            self.count += 1
            if self.status_bar == True:
                self.qbar.update()
            return text
        else:
            self.count = 0
            raise StopIteration
        
    def cache(self, file):
        """
        Parameters
        ----------
        file : string
            The path of the file that is to be cached

        Returns
        -------
        None.
        
        We build this function so that the same instance of a Fast_File
        may be used for a sequence of files. One just needs to cache them
        sequentially.
        """
        assert os.path.exists(file), "File not found"
        self.file = file
        self.linepoints = deque()
        self.linepoints.append(-1)
        with open(file,'r+', encoding='utf-8') as fp:
            mm = mmap.mmap(fp.fileno(),0 )        
            # This loop iterates through the file and appends each position
            # of an endline character. 
            qbar = tqdm(range(os.path.getsize(self.file)))
            for i in qbar:
                c = mm[i:i+1].decode()
                if not c:
                    break
                if c == '\n':
                    self.linepoints.append(i)
                    # This is due to the endline being preceeded by the 
                    # linebreak.
                    
                    if len(self.linepoints) % 1000 == 0:
                        qbar.set_description("{} lines read".format(len(self.linepoints)))
        self.fp = open(self.file,'r+', encoding='utf-8')
        self.mm = mmap.mmap(self.fp.fileno(),0 )
        self.linepoints.append(i)
        self.linepoints = list(self.linepoints)
        if self.shuffle == True:
            self.order = list(range(len(self)))
            random.shuffle(self.order)
        else:
            self.order = list(range(len(self)))
    
    def __getitem__(self, index):
        return self.getline(index)
    
    def getline(self, i):
        """
        Parameters
        ----------
        i : int
            The line number of the text that needs to be returned.

        Returns
        -------
        str or bytes
            Return the i-th line of the file

        """
        out = self.mm[self.linepoints[i]+1:self.linepoints[i+1]]
        if self.string == True:
            return out.decode("utf-8", "ignore")
        else:
            return out
    
    def __len__(self):
        return len(self.linepoints)-2
    
    def close(self):
        self.mm.close()
        self.fp.close()
        
    def save(self, path):
        np.save(path, (self.file, self.linepoints))
        
    def load(self, path):
        self.file, self.linepoints = np.load(path, allow_pickle= True)
        self.fp = open(self.file,'r+')
        self.mm = mmap.mmap(self.fp.fileno(),0 )
        self.order = list(range(len(self)))

                
