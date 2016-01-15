__author__ = 'egreat'

# coding from William's ReadData.py

import pandas as pd
import tushare as ts
import datetime
import os
#from sympy.physics.units import days
WINDOW = 500

'globally make a /data folder'
path = 'data'
if(not os.path.isdir(path)):
    os.mkdir(path)

'make a /data/raw folder, and return the .csv file under it'
def FilePath(code):
    path = 'data\\Raw\\'
    if(not os.path.isdir(path)):
        os.mkdir(path)
    return path+code +'.csv'

'''
def PairPath(code1, code2):
    path = 'data\\pairs\\'
    if(not os.path.isdir(path)):
        os.mkdir(path)
    return path+ code1 + '_' + code2+ '.csv'
'''

def GetTime(nDaysAgo=0):
    theTime = (datetime.datetime.now() - datetime.timedelta(days = nDaysAgo))
    return theTime.strftime("%Y-%m-%d")

def fetch_data(code, win_len):
    if(os.path.isfile(FilePath(code))):
        df = pd.read_csv(FilePath(code), encoding='utf-8')
    else:
        df = ts.get_h_data(code[2:], start=GetTime(win_len), end=GetTime())
        df = df.sort_index(axis=0, ascending=True)
        df.to_csv(FilePath(code), encoding='utf-8')
    return df

def load_stock(code):
    global WINDOW
    return fetch_data(code, WINDOW)

def save_stock(code, data):
    data.to_csv(FilePath(code))
    return FilePath(code)

def load_pair(codey, codex):
    return pd.read_csv(PairPath(codey, codex), index_col=0)
def save_pair(codey, codex, data):
    data.to_csv(PairPath(codey, codex))
    return PairPath(codey, codex)

class Summary():
    def __init__(self):
        self.csv = 'pair_data_summary.csv'
        if(os.path.isfile(self.csv)):
            self.df = pd.read_csv(self.csv, index_col=0)
        else:
            self.df = pd.DataFrame()
    def load(self):
        return self.df
    def save(self, df):
        df.to_csv(self.csv)

    def append(self, iloc, col, value ):
        self.df[iloc,col] = value


