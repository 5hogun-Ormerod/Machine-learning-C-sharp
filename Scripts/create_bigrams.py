import pandas as pd
import sys

sys.path.append("c:/GIT/NLP-Ormerod")

from Utils import Fast_File
import spacy
import string
from collections import Counter, deque
from tqdm import tqdm
import numpy as np

nlp = spacy.load('en')

doc = pd.read_csv("c:/data/corpus/aspell_dict.txt", header=None, delimiter="\t")

words = set(doc[doc[0].map(lambda x:str(x).islower())][0].iloc[16:])

for p in string.punctuation:
    words.add(p)
    
for p in ["'s", "n't", "'re","'ll","'d","'ve", '[num]','[propn]','ok']:
    words.add(p)

FF = Fast_File()
FF.load("c:/data/corpus/lower.ff.npy")

def is_num(token):
    try:
        num = float(token)
        return '[num]'
    except:
        return token
    
def tokenize(text):
    doc = nlp(text, disable=['ner','parser'])
    tokens = [str(x) if x.pos_ != 'PROPN' else '[propn]' for x in doc]
    tokens = [is_num(x) for x in tokens]
    return tokens
    
count = Counter()

i = 0

for text in FF:
    i = i +1
    bag = deque(maxlen = 2)
    tokens = tokenize(text)
    for t in tokens:
        if t in words:
            bag.append(t)
            if len(bag) > 1:
                b = ' '.join(bag)
                count[b] = count[b] + 1
                count[t] = count[t] + 1
            else:
                count[t] = count[t] + 1
        else:
            bag.clear()
            
    if i % 1000000 == 0:
        np.save("c:/data/stuff.npy",count)