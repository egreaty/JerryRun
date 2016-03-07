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
import logging
# import seaborn

from talib import MA_Type

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''
cwd = os.getcwd()
parent_wd = cwd[0:-5]
sys.path.append(parent_wd + '\\fileio')
print "current dir is " + parent_wd
sys.path.append(parent_wd + '\\runrun\\filoio')
'''

stock_lytz = '600784'
stock_sdhj = '600547'

stock_list = [stock_sdhj, stock_lytz]
stock_code = stock_list

for stock in stock_code:
    logger.info('begin processing stock %s', stock)
    raw_stock_info = sd.get_stock_data(stock)
    stock_close = raw_stock_info[0].ix[:, 'close']

# stock_short = raw_stock_info[0].ix[:, 'ma5']
obj_data = np.array(stock_close, dtype=pd.Series)

float_data = [float(x) for x in obj_data]  # convert pd obj_data to float data which while be used by talib
np_float_data = np.array(float_data)

mean = talib.SMA(np_float_data)
upper, middle, lower = talib.BBANDS(np_float_data, matype=MA_Type.T3)
output = talib.MOM(np_float_data, timeperiod=5)

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(stock_close)
ax.plot(mean)
ax.plot(upper)
ax.plot(middle)
ax.plot(lower)
plt.show()
