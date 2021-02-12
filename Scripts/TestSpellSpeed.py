import numpy as np
from heapq import nlargest
import string
import random
import pandas as pd
from time import time
from Spelling.Norvig import norvig_correct_word

count = np.load("C:/data/corpus/new_2grams.npy", allow_pickle= True).all()

from Spelling.Dictionary import words

ss = pd.read_excel("c:/data/essays/single_scored_cleaned.xlsx")
oov = ss['response'].map(lambda x:str(x).lower().split()).map(lambda text: [x for x in text if x not in words and len(x) > 3 and  x.isalpha()])

test = sum(oov.iloc[:157],list())

topn = lambda n:dict(nlargest(n, count.items(),key =lambda x:x[1]))

from Spelling.VocabTreeNode import VocabTreeNode
from Spelling.BKTree import BKTree

from tqdm import tqdm

def get_random_string():
    length = random.randint(4,16)
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#test = [get_random_string() for _ in range(1000)]


record = pd.DataFrame()

# for size in range(1,51):

#     vocab = topn(10000*size)
    
#     results = {"vocab size": len(vocab)}
    
#     start = time()
#     T = VocabTreeNode(vocab)
#     results['VT build'] = time()-start
    
#     start = time()
#     BK = BKTree(vocab)
#     results['BK build'] = time()-start

#     start = time()
#     print("Speed Test Norvig 1")
#     for t in test:
#         res = norvig_correct_word(t, vocab, 1)
#     results['N ed1'] = (time()-start)/len(test)    

#     start = time()
#     print("Speed Test Norvig 2")
#     for t in test:
#         res = norvig_correct_word(t, vocab, 2)
#     results['N ed2'] = (time()-start)/len(test) 

#     start = time()
#     print("Speed Test VocabTreeNode")
#     for t in test:
#         res = T.candidates(t,1)
#     results['VT ed1'] = (time()-start)/len(test)    

#     start = time()
#     print("Speed Test VocabTreeNode")
#     for t in test:
#         res = T.candidates(t,2)
#     results['VT ed2'] = (time()-start)/len(test) 
    
#     start = time()
#     print("Speed Test VocabTreeNode")
#     for t in test:
#         res = T.candidates(t,3)
#     results['VT ed3'] = (time()-start)/len(test)


        
#     start = time()
#     print("Speed Test BKTree")
#     for t in test:
#         res = BK.search(t,1)
#     results['BK ed1'] = (time()-start)/len(test)    

#     start = time()
#     print("Speed Test BKTree")
#     for t in test:
#         res = BK.search(t,2)
#     results['BK ed2'] = (time()-start)/len(test) 
    
#     start = time()
#     print("Speed Test BKTree")
#     for t in test:
#         res = BK.search(t,3)
#     results['BK ed3'] = (time()-start)/len(test)
    
#     print(results)
    
#     record = pd.concat([record, pd.DataFrame(results,index=[len(record)])])

from subprocess import Popen, PIPE

aspell_process = Popen(['c:/Aspell/bin/aspell.exe','-a'],
                       stdin=PIPE,
                       stdout=PIPE,
                       stderr=PIPE,
                       shell=True)

output = aspell_process.stdout.readline()

results = {}

def Aspell(word):
    inp = word + "\n"
    aspell_process.stdin.write(inp.encode())
    aspell_process.stdin.flush()
    output = aspell_process.stdout.readline()
    aspell_process.stdout.readline()
    if output == b'*\r\n':
        return [word]
    else:
        s = output.decode()
        try:
            L = s[s.index(":")+1:].split(",")
            return [x.strip() for x in L]
        except:
            return [word]

start = time()
print("Aspell")
for t in test:
    cost = min(max(int(np.floor(len(t)/2)),1),6)
    res = Aspell(t)
results['Aspell'] = (time()-start)/len(test)

print(results)


vocab = topn(10000*12)
results = {"vocab size": len(vocab)}

start = time()
T = VocabTreeNode(vocab)
results['VT build'] = time()-start

start = time()
BK = BKTree(vocab)
results['BK build'] = time()-start    
    

start = time()
print("BK")
for t in test:
    cost = min(max(int(np.floor(len(t)/2)),1),6)
    res = BK.search(t,cost)
results['BK'] = (time()-start)/len(test)

start = time()
print("Speed Test VocabTreeNode")
for t in test:
    cost = min(max(int(np.floor(len(t)/2)),1),6)
    res = T.candidates(t,cost)
results['VT'] = (time()-start)/len(test) 

print(results)

def tikzify(xaxis, yaxis_list, xlabel,ylabels_list):
    xmax = max(xaxis)
    xmin = min(xaxis)
    ymax = max(sum(yaxis_list,list()))
    ymin = min(sum(yaxis_list,list()))
    
    scalepoints = lambda x,y: (10*(x-xmin)/(xmax-xmin),10*y/ymax)

    
    print("\\begin{tikzpicture}\n\\draw (0,0)--(10,0);\n\\draw (0,0)--(0,10);")
    for i in range(6):
        print("\\node at (-1,{}) {{{}}};".format(2*i, ymin + i*(ymax-ymin)/5))
        print("\\node at ({},-1) {{{}}};".format(2*i, xmin + i*(xmax-xmin)/5))
    for yaxis in yaxis_list:
        print("\\draw ({},{})".format(*scalepoints(xaxis[0],yaxis[0])), end="")
        for k,(x,y) in enumerate(zip(xaxis[1:],yaxis[1:])):
            print("--({},{})".format(*scalepoints(x,y)),end = "")
        print(";")
    