__author__ = 'egreat'

'''
fix kw warning
'''

import sys
import os
import wechat
import stockData as sd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib
import zipline

# import seaborn

'''
cwd = os.getcwd()
parent_wd = cwd[0:-5]
sys.path.append(parent_wd + '\\fileio')
print "current dir is " + parent_wd
sys.path.append(parent_wd + '\\runrun\\filoio')
'''

stock_lytz = '600784'
stock_sdhj = '600547'

stock_code = [stock_lytz, stock_sdhj]

for stock in stock_code:
    raw_stock_info = sd.fetch_stock_data(stock)
    stock_close = raw_stock_info[0].ix[:, 'close']

# stock_short = raw_stock_info[0].ix[:, 'ma5']
obj_data = np.array(stock_close,dtype=pd.Series)

float_data = [float(x) for x in obj_data]
np_float_data = np.array(float_data)

mean = talib.SMA(np_float_data)

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(stock_close)
ax.plot(mean)
plt.show()
