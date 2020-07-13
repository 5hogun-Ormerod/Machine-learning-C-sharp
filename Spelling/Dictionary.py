import pandas as pd

words = set(pd.read_csv("c:/Data/corpus/words.txt",header=None)[0].map(str).map(lambda x:x.lower()))

