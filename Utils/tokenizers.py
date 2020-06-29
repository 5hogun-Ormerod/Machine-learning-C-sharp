# From experimentation, these are the fastest

from nltk.tokenize import RegexpTokenizer

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

