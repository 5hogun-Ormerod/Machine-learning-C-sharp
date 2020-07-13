import pandas as pd
import os
from Utils.tokenizers import tokenize

files = os.listdir("C:/GIT/HankenCorpus/plain/")

Hankel = pd.concat([pd.read_csv("C:/GIT/HankenCorpus/plain/{}".format(f), sep='\n',encoding= 'unicode_escape', header=None) for f in files], ignore_index=True)[0]

Hankel = Hankel[Hankel.map(tokenize).map(len) > 4]
