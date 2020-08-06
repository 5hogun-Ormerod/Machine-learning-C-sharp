# From experimentation, these are the fastest

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import sent_tokenize
import io
from fileaccess import Fast_File
from NeuralNetworks.core.tokenizer import tokenizer

import sentencepiece

    
class word_tokenizer()
    
    def __init__(self):
        self.__pattern = r'''(?x)       
                        (?:[A-Z]\.)+      
                        | \w+(?:-\w+)*     
                        | \$?\d+(?:\.\d+)?%? 
                        | \.\.\.           
                        | [][.,;"'?():_`-]  
                        '''
    
        self.__tokenizer = RegexpTokenizer(__pattern)
        self.__detokenizer = TreebankWordDetokenizer()

    def tokenize(self, text):
        return self..__tokenizer.tokenize(text)

    def detokenize(self, iterable):
        return self.__detokenizer.detokenize(iterable)
    
    def encode(self, text):
        pass
    
    def decode(self, iterable):
        pass

    def vocab(self):
        return None
    
class character_tokenizer(self):
    
    def __init__(self):
        pass
    
    



class BPE_tokenizer(tokenizer):
    
    def __init__(self, lower = False, vocab_size = 1000):
        model = io.BytesIO()
        self.vocab_size = vocab_size
        
    def __fit_file(self, file):
        self.source_file = file
        with Fast_File(file) as ff:
            self.__fit_iterable(ff)
            
    def __fit_iterable(self, it):
        sentencepiece.SentencePieceTrainer.train(sentence_iterator=it, 
                                                 model_writer=self.model, 
                                                 vocab_size=self.vocab_size)
            
    def fit(self, x):
        if isinstance(x, string):
            self.__fit_file(x)
        else:
            self.__fit_iterable(x)
            
    def tokenize(self, text):
        return self.model.