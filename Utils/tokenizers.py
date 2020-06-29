# From experimentation, these are the fastest

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

__pattern = r'''(?x)       
        (?:[A-Z]\.)+      
      | \w+(?:-\w+)*     
      | \$?\d+(?:\.\d+)?%? 
      | \.\.\.           
      | [][.,;"'?():_`-]  
    '''

__tokenizer = RegexpTokenizer(__pattern)

def tokenize(text):
    return __tokenizer.tokenize(text)

def detokenize(iterable):
    return TreebankWordDetokenizer().detokenize(iterable)

