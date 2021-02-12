import sys

sys.path.append("/home/cormerod/RemoteProjects/NLP")

from Utils import Fast_File
from Utils import word_tokenizer



with open("c:/data/corpus/refined.txt",'w') as fp:
    for i in tqdm(range(len(FF))):
        if ((len(FF[i]) > 400) and (len(FF[i]) < 4000)):
            fp.write(FF[i])
            fp.write("\n")
            
    