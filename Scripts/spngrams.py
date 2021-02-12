# -*- coding: utf-8 -*-

from Utils.fileaccess import Fast_File
from collections import deque, Counter
import sentencepiece as sp
from tqdm import tqdm

tokenizer = sp.SentencePieceProcessor("c:/data/Embeddings/wordpiece/BPE_lower8k.model")

FF = Fast_File()
FF.load("c:/data/corpus/lower.ff.npy")

count = 0

trigrams = Counter()

with tqdm(FF) as qbar:
    for text in qbar:
        count += 1
        bag3 = deque(maxlen=3)
        bag2 = deque(maxlen=2)
        tokens = tokenizer.EncodeAsPieces(text)
        for t in tokens:
            bag3.append(t)
            bag2.append(t)
            
            tri  =' '.join(bag3)
            bi  =' '.join(bag2)
            trigrams[tri] = trigrams[tri] + 1            
            trigrams[bi] = trigrams[bi] + 1
            trigrams[t] = trigrams[t] + 1
        if count % 20000 == 0:
            qbar.set_description("{} 3grams".format(len(trigrams)))