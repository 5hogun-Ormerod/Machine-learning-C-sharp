from Utils import sentencepiece_tokenizer

t = sentencepiece_tokenizer()
t.load("c:/models/sentencepiece/BPE_cased16k.model")

def compress(text):
    enc = t.sp.EncodeAsIds(text)
    
    out = b''
    
    mem = ''
    
    for i in enc:
        rep = bin(i)[2:]
        rep = '0'*(14-len(rep)) + rep
        mem += rep
        while len(mem) > 8:
            piece = mem[:8]
            mem = mem[8:]
            piece = int(piece, 2).to_bytes(1, 'little')
            out += piece
    mem = mem + '0'*(8-len(mem))
    piece = int(mem, 2).to_bytes(1, 'little')
    out += piece
    return out
