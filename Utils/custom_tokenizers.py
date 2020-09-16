# From experimentation, these are the fastest

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import sent_tokenize
import io
from Utils import Fast_File
from core.tokenizer import tokenizer
import gensim
import sentencepiece

    
class word_tokenizer(tokenizer):
    
    def __init__(self):
        self.__pattern = r'''(?x)       
                        (?:[A-Z]\.)+      
                        | \w+(?:-\w+)*     
                        | \$?\d+(?:\.\d+)?%? 
                        | \.\.\.           
                        | [][.,;"'?():_`-]  
                        '''
    
        self.__tokenizer = RegexpTokenizer(self.__pattern)
        self.__detokenizer = TreebankWordDetokenizer()

    def tokenize(self, text):
        return self.__tokenizer.tokenize(text)

    def detokenize(self, iterable):
        return self.__detokenizer.detokenize(iterable)
    
    def encode(self, text):
        pass
    
    def decode(self, iterable):
        pass

    def vocab(self):
        return 0
    
    def __fit_file(self, file):
        self.source_file = file
        with Fast_File(file) as ff:
            self.__fit_iterable(ff)
            
    def __fit_iterable(self, it):
        sentencepiece.SentencePieceTrainer.Train(sentence_iterator=it, 
                                                 model_writer=self.model)    
    
    def fit(self, x):
        if isinstance(x, str):
            self.__fit_file(x)
        else:
            self.__fit_iterable(x)

class split_tokenizer(tokenizer):
    
    def __init__(self):
        pass
    
    def tokenize(self, text):
        return text.split()

    def detokenize(self, iterable):
        return ' '.join(iterable)

    def fit(self, iterable):
        pass
    
    def encode(self, text):
        pass
    
    def decode(self, iterable):
        pass

    def vocab(self):
        return 0
        
class character_tokenizer(tokenizer):
    
    def __init__(self):
        pass
    
    def tokenize(self, text):
        return list(text)

    def detokenize(self, iterable):
        return ''.join(iterable)
    
    def encode(self, text):
        enc = [x+2 for x in text.encode()]
        return enc
    
    def decode(self, iterable):
        dec = bytes([x -2 for x in iterable]).decode()
        return dec
       
    def vocab(self):
        return list(bytes(range(128)).decode())
        
    def vecotrize(self, iterable):
        pass


class sentencepiece_tokenizer(tokenizer):
    
    def __init__(self, lower = False, vocab_size = 1000):
        self.model = io.BytesIO()
        self.vocab_size = vocab_size
        
    def __fit_file(self, file):
        self.source_file = file
        with Fast_File(file) as ff:
            self.__fit_iterable(ff)
            
    def __fit_iterable(self, it):
        sentencepiece.SentencePieceTrainer.train(sentence_iterator=it, 
                                       model_writer=self.model, 
                                       vocab_size=self.vocab_size)
        self.sp = sentencepiece.SentencePieceProcessor(model_proto=self.model.getvalue())
            
    def fit_vectorizor(self, x):
        if isinstance(x, str):
            self.__fit__file(x)
        else:
            self.__fit_iterable(x)
            
    def __fit_vectorizer_file(self, file):
        self.source_file = file
        with Fast_File(file) as ff:
            self.__fit_iterable(ff)
            
    def __fit_iterable(self, it):
        sentencepiece.SentencePieceTrainer.train(sentence_iterator=it, 
                                       model_writer=self.model, 
                                       vocab_size=self.vocab_size)
        self.sp = sentencepiece.SentencePieceProcessor(model_proto=self.model.getvalue())
            
    def fit(self, x):
        """
        Parameters
        ----------
        x : str or Iterable
            If the type is a str, we assumed that string is a path to a file
            with text in it, hence, is handled by the Fast_File class, else
            it is to be handled directly as an TextSet.

            This fit command should fit the optimal encoding using googles 
            sentencepiece encoding.
        """
        if isinstance(x, str):
            self.__fit_file(x)
        else:
            self.__fit_iterable(x)
            
    def tokenize(self, text):
        return self.sp.encode(text,
                              truncation=True,
                              max_length = 1024,
                              padding='max_length')
    
    def encode(self, text):
        pass
    
    def load(self, path):
        self.sp = sentencepiece.SentencePieceProcessor(path)

    def save(self, path):
        pass    
    

