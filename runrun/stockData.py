# -*- coding:utf-8 -*-
'''
Created on 2016/1/13
@author: Jerry Bai
* get data from file or db
* get data from yahoo?
* get data via tushare

* save date in file or db

No matter where data got, when storing in file, they unified in the same format when saving.
    Here we can consider using db to store data for future access

When trying got data, first examine db or file, if not exist, got it from web and save it

'''

import os
import time
import pandas as pd
import tushare as ts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cwd = os.getcwd()
default_data_path = cwd + '\\Stock\\'

ONE_HOUR_IN_SEC = 60 * 60


'''
api for top level get data
it will internally decide if get if from tushare or local
'''


def get_stock_data(code, data_path=None):
    logger.debug('begin of fetch_stock_data()')

    if data_path is None:
        data_file = default_data_path + code + '.csv'
    else:
        data_file = data_path + code + '.csv'

    logger.debug('data_file is %s', data_file)

    if os.path.isfile(data_file):
        if get_file_age(data_file) < (8 * ONE_HOUR_IN_SEC):  # TODO: change to check if the last record is today
            stock_df = pd.read_csv(data_file, encoding='utf-8')
            logger.info("read data from local file")

    try:  # alternative: if 'myVar' in locals():
        stock_df
    except NameError:  # if stock_df not exist, get it from tushare
        stock_df = ts.get_h_data(code, autype='qfq')
        stock_df = stock_df.sort_index(axis=0, ascending=True)
        stock_df.to_csv(data_file)

    return [stock_df, data_file]


def get_file_age(file_name):
    modify_time_in_sec = os.path.getmtime(file_name)
    curr_time_in_sec = time.time()

    logger.debug("last modified: %s" % time.ctime(modify_time_in_sec))
    logger.debug("current time %s" % time.ctime(curr_time_in_sec))

    assert (curr_time_in_sec >= modify_time_in_sec)
    return curr_time_in_sec - modify_time_in_sec