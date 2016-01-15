__author__ = 'egreat'

'''
fix kw warning
'''

import stockData as sd
import pandas as pd
import matplotlib.pyplot as plt
import tushare
# import zipline
# import seaborn

stock_lytz = '600784'
stock_sdhj = '600547'


raw_stock_info = sd.fetch_stock_data(stock_sdhj)

stock_close = raw_stock_info[0].ix[:, 'close']

#stock_short = raw_stock_info[0].ix[:, 'ma5']

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(stock_close)
plt.show()
