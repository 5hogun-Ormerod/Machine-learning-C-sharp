from fastai.collab import *
from fastai.tabular import *
import pandas as pd
from sklearn.model_selection import train_test_split
from nlp import load_dataset
from NeuralNetworks.core.nn_dataset import DataFrameSet


def convert_path(path, columns):
    train = pd.read_csv('{}/train.csv'.format(path), header = None) 
    val = pd.read_csv('{}/test.csv'.format(path), header = None)
    train.columns = columns
    val.columns = columns
    train, test = train_test_split(train, test_size = 0.2 ,random_state = 1)
    
    return {'train': DataFrameSet(train),
            'test':DataFrameSet(test),
            'validation':DataFrameSet(val)}
  

def get_amazon_reviews():
    columns = ['score', 'title', 'text']
    path = untar_data(URLs.AMAZON_REVIEWS)
    return convert_path(path)

def get_wiki_103():
    columns = ['text']
    path = untar_data(URLs.WIKITEXT)
    return convert_path(path, columns)

gigaword = lambda : load_dataset('gigaword')

squadv2 = lambda :load_dataset('squad_v2')

def kaggle_aes(essay, fold):
    assert split in range(5), "Split out of range"
    assert essay in range(1,9), "Essay number out of range"
    
    train_ids = set(pd.read_csv("c:/data/kaggle/splits/fold_{}/train_ids.txt".format(split), header = None)[0])
    test_ids = set(pd.read_csv("c:/data/kaggle/splits/fold_{}/test_ids.txt".format(split), header = None)[0])
    validation_ids = set(pd.read_csv("c:/data/kaggle/splits/fold_{}/dev_ids.txt".format(split), header = None)[0])
    
    data = pd.read_excel("c:/data/kaggle/training_set_rel3.xlsx")
    
    train = data[(data['essay_id'].map(lambda x:x in train_ids)) & (data['essay_set'] == essay)]
    test = data[(data['essay_id'].map(lambda x:x in test_ids)) & (data['essay_set'] == essay)]
    val = data[(data['essay_id'].map(lambda x:x in validation_ids)) & (data['essay_set'] == essay)]
    
    return {'train': DataFrameSet(train),
            'test':DataFrameSet(test),
            'validation':DataFrameSet(val)}