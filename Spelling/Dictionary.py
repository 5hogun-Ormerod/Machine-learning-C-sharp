import ujson
from collections import Counter

with open("C:/data/word_count.json",'r') as fp:
    word_counter = Counter(ujson.load(fp))