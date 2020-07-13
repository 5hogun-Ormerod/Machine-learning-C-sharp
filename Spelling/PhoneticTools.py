import nltk
import string
from Spelling import words
from Utils import tokenize

word_to_phonemes = nltk.corpus.cmudict.dict()

def build_w2p():
    wordlist = list(word_to_phonemes)
    phonemes_to_word = dict()
    for w in wordlist:
        for p in word_to_phonemes[w]:
            s = ' '.join(p)
            if s not in phonemes_to_word:
                phonemes_to_word[s] = [w]
            else:
                phonemes_to_word[s].append(w)
    return phonemes_to_word

phonemes_to_word = build_w2p()

def word_break_choices(word):
    if word in word_to_phonemes:
        possibilities = [[word]]
    else:
        # here we need to guess how to pronounce a word by breaking it up
        possibilities = []
        for i in range(len(word)):
        
            word_left = word[:i]
            word_right = word[i:]
            if word_left in word_to_phonemes:
                right_possiblities = word_break_choices(word_right)
                for r in right_possiblities:
                    possibilities.append([word_left]+r)
    return possibilities

def word_break(word):
    possibilities = word_break_choices(word)
    if len(possibilities) > 0: 
        length = min([len(x) for x in possibilities])
        least_length = [p for p in possibilities if len(p) == length]
        return least_length[0]
    else:
        return [word]

def text_to_phonemes(text):
    pause_tokens = string.punctuation
    tokens = tokenize(text.lower())
    tokens = [['[L]'] if t in pause_tokens else word_break(t) for t in tokens ]
    broken_phonemes = [t[0] if t == ['[L]'] else ' '.join(sum([word_to_phonemes[x][0] for x in t],list())) for t in tokens]
    sounds = ' [P] '.join(broken_phonemes).replace('[P] [L] [P]','[L]').replace('[P] [L]','[L]')
    return sounds

phonetic_errors = {k: sum([phonemes_to_word[' '.join(x)] for x in word_to_phonemes[k]],list()) for k in word_to_phonemes if (k in words) and len(set(sum([phonemes_to_word[' '.join(x)] for x in word_to_phonemes[k]],list()))) > 1}


