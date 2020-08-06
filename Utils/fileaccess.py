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

class Fast_File(object):
    
    # This is a wrapper for the process of enumerating the endlines of a 
    # file, then accessing lines using the mmap function. This is essentially
    # a faster version of the linecache which is slightly faster than 
    # linecache while performing approximately the same function up to
    # conversion from bytes to string.
    
    def __init__(self, 
                 file = None,
                 shuffle = True,
                 status_bar = True,
                 string = True):
        
        self.shuffle = shuffle
        self.status_bar = status_bar
        self.string = string
        
        if file is not None:
            self.cache(file)
        self.count = 0
            
    def __iter__(self):
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self,  arg_type, value, traceback):
        self.close()
    
    def __next__(self):
        if self.count == 0:
            self.qbar = tqdm(range(len(self)-1))
        if self.count < len(self):
            text = self.getline(self.order[self.count])
            self.count += 1
            if self.status_bar == True:
                self.qbar.update()
            return text
        else:
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
        self.linepoints.append(0)
        pos = 0
        with open(file,'r') as fp:
            
            # This loop iterates through the file and appends each position
            # of an endline character. 
            qbar = tqdm(range(os.path.getsize(self.file)))
            for _ in qbar:
                c = fp.read(1)
                if not c:
                    break
                if c == '\n':
                    self.linepoints.append(pos)
                    pos += 1
                    # This is due to the endline being preceeded by the 
                    # linebreak.
                    
                    if len(self.linepoints) % 1000 == 0:
                        qbar.set_description("{} lines read".format(len(self.linepoints)))
                pos += 1
        self.fp = open(self.file,'r+')
        self.mm = mmap.mmap(self.fp.fileno(),0 )
        self.linepoints.append(pos)
        self.linepoints = list(self.linepoints)
        if self.shuffle == True:
            self.order = list(range(len(self)))
            random.shuffle(self.order)
        else:
            order = list(range(len(self)))
                
    def getline(self, i):
        """
        Parameters
        ----------
        i : int
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        out = self.mm[self.linepoints[i]+2:self.linepoints[i+1]]
        if self.string == True:
            return str(out)
        else:
            return out
    
    def __len__(self):
        return len(self.linepoints)-1
    
    def close(self):
        self.mm.close()
        self.fp.close()
        
    def save(self, path):
        np.save(path, (self.file, self.linepoints))
        
    def load(self, path):
        self.file, self.linepoints = np.load(path, allow_pickle= True)
        self.fp = open(self.file,'r+')
        self.mm = mmap.mmap(self.fp.fileno(),0 )

                
      