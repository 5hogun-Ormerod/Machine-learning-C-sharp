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

class fast_file():
    
    #
    #
    
    def __init__(self, file = None):
        if file is not None:
            self.cache(file)
        
    def cache(self, file):
        assert os.path.exists(file), "File not found"
        self.file = file
        self.linepoints = deque()
        self.linepoints.append(0)
        pos = 0
        with open(file,'r') as fp:
            for _ in tqdm(range(os.path.getsize(self.file))):
                c = fp.read(1)
                if not c:
                    break
                if c == '\n':
                    self.linepoints.append(pos)
                    pos += 1
                pos += 1
        self.fp = open(self.file,'r+')
        self.mm = mmap.mmap(self.fp.fileno(),0 )
        self.linepoints.append(pos)
                
    def getline(self, i):
        return self.mm[self.linepoints[i]+2:self.linepoints[i+1]]
    
    def __len__(self):
        return len(self.linepoints)-1
    
    def close(self):
        self.mm.close()
        self.fp.close()
        
    def save(self, path):
        np.save(path, (self.file, linepoints))
        
    def load(self, path):
        self.file, self.linepoints = np.load(path, allow_pickle)
        self.fp = open(self.file,'r+')
        self.mm = mmap.mmap(self.fp.fileno(),0 )

                
      