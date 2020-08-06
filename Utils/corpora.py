from fastai.collab import *
from fastai.tabular import *
import pandas as pd


def get_amazon_reviews():
    path = untar_data(URLs.AMAZON_REVIEWS)
    columns = ['score', 'title', 'text']
    train = pd.read_csv('{}/train.csv'.format(path), header = None) 
    test = pd.read_csv('{}/test.csv'.format(path), header = None)
    train.columns = columns
    test.columns = columns
    
    return train, test