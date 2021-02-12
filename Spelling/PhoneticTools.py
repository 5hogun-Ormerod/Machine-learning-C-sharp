from metaphone import doublemetaphone
from Spelling import EditDistance

dm = lambda x:doublemetaphone(str(x).replace("'",""))

def phonetic_representation(word):
    
    tokens = word.split()
    return recursive_representation(tokens)
    
def recursive_representation(tokens):    
    
    if len(tokens) == 1:
        return {p for p in dm(tokens[0]) if p != ""}
    else:
        rephead = {p for p in dm(tokens[0]) if p != ""}
        reptail = recursive_representation(tokens[1:])
        return {h + ' ' + t  for h in rephead for t in reptail}
    
def phonetic_distance(s1, s2):
    rep1 = phonetic_representation(s1)
    rep2 = phonetic_representation(s2)
    return phonetic_rep_distance(rep1,rep2)

def phonetic_onesided_distance(rep1, s2):
    rep2 = phonetic_representation(s2)
    return phonetic_rep_distance(rep1,rep2)
    

def phonetic_rep_distance(rep1, rep2):
    return min({EditDistance(r1,r2) for r1 in rep1 for r2 in rep2})