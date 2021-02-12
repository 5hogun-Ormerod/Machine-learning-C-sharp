from tqdm import tqdm
import glob

def TXTsearch(directory):
    
    text_files = glob.glob(directory + "/**/*.txt", recursive = True)
    
    rows = []
    
    for txtfile in tqdm(text_files):
        with open(txtfile,'r',encoding="utf8") as fp:
            for line in fp:
                try:
                    if len(line.strip()) > 2:
                        print(line.strip())
                        rows.append(line.strip())
                except:
                    pass
                
    return rows