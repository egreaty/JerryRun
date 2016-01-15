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

data_path = 'Stock\\'

ONE_HOUR_IN_SEC = 60 * 60


def fetch_stock_data(code, data_csv=None):
    print("log: begin of fetch_stock_data()")

    if data_csv is None:
        data_csv = data_path + code + '.csv'

    if not os.path.isfile(data_csv):
        stock_df = get_tushare_data_and_store(code, data_csv)
    else:
        file_last_modify_time_in_sec = os.path.getmtime(data_csv)
        curr_time_in_sec = time.time()
        print "last modified: %s" % time.ctime(file_last_modify_time_in_sec)
        print "current time %s" % time.ctime(curr_time_in_sec)

        assert (curr_time_in_sec >= file_last_modify_time_in_sec)

        if curr_time_in_sec - file_last_modify_time_in_sec > ONE_HOUR_IN_SEC: # TODO: Here change it to check the data_csv, if the last line is today's
            stock_df = get_tushare_data_and_store(code, data_csv)
        else:
            stock_df = pd.read_csv(data_csv, encoding='utf-8')
            print("log: read data from local file")

    return [stock_df, data_csv]


def get_tushare_data_and_store(code, data_csv):
    stock_df = ts.get_h_data(code, autype='qfq')
    stock_df = stock_df.sort_index(axis=0, ascending=True)
    stock_df.to_csv(data_csv)
    print("log: get data via tushare")

    return stock_df


def getFeatureSample(StockDf, idx, colum_name, feature_id):
    feature_val = StockDf.ix[idx, colum_name]
    sample = str(feature_id) + ':' + str(feature_val) + ' '
    return sample


def fetch_stock_data_obsolete(code, output_csv=None):
    StockDf = ts.get_h_data(code)
    StockDf = StockDf.sort_index(axis=0, ascending=True)
    # adding EMA feature
    StockDf['ema'] = StockDf['close']
    StockDf['rise'] = StockDf['close']
    DfLen = len(StockDf.index)
    EMA = 0;
    RISE = 0;
    for n in range(0, DfLen):
        idx = n
        Close = StockDf.ix[idx, 'close']
        if (n == 0):
            EMA = Close
            RISE = 0
        else:
            EMA = StockDf.ix[idx - 11, 'ema']
            EMA = ((n - 1) * EMA + 2 * Close) / (n + 1)
            CloseP = StockDf.ix[idx - 1, 'close']
            RISE = (Close - CloseP) / CloseP

        StockDf.ix[idx, 'ema'] = EMA
        StockDf.ix[idx, 'rise'] = RISE

    if (output_csv != None):
        StockDf.to_csv(output_csv)

    return StockDf


def genFeature(StockDf, file_name, win_size=3):
    # Generating moving window features
    print file_name
    problem_file = open(file_name, 'w+')
    DfLen = len(StockDf.index)
    for n in range(0, DfLen - win_size):
        predic_idx = n + win_size
        predict = 0
        predict = StockDf.ix[predic_idx, 'rise']
        predict = predict * 10  # 1= rise 10%
        Sample = str(predict) + ' '

        feature_id = 1
        feature_val = 0
        for j in range(n, n + win_size):
            Sample += getFeatureSample(StockDf, j, 'open', feature_id)
            feature_id += 1
            Sample += getFeatureSample(StockDf, j, 'high', feature_id)
            feature_id += 1
            Sample += getFeatureSample(StockDf, j, 'close', feature_id)
            feature_id += 1
            Sample += getFeatureSample(StockDf, j, 'low', feature_id)
            feature_id += 1
            Sample += getFeatureSample(StockDf, j, 'volume', feature_id)
            feature_id += 1
            Sample += getFeatureSample(StockDf, j, 'ema', feature_id)
            feature_id += 1

        Sample += '\n'
        problem_file.write(Sample)

    problem_file.close()
    print('\n sample number: ' + str(n + 1) + '\n feature number: ' + str(feature_id - 1))

    del problem_file
    # del StockDf


def genTest(StockDf, file_name, win_size=3):
    problem_file = open(file_name, 'w+')
    predict = 0
    Sample = str(predict) + ' '
    DfLen = len(StockDf.index)
    n = DfLen - win_size

    feature_id = 1
    feature_val = 0
    for j in range(n, n + win_size):
        Sample += getFeatureSample(StockDf, j, 'open', feature_id)
        feature_id += 1
        Sample += getFeatureSample(StockDf, j, 'high', feature_id)
        feature_id += 1
        Sample += getFeatureSample(StockDf, j, 'close', feature_id)
        feature_id += 1
        Sample += getFeatureSample(StockDf, j, 'low', feature_id)
        feature_id += 1
        Sample += getFeatureSample(StockDf, j, 'volume', feature_id)
        feature_id += 1
        Sample += getFeatureSample(StockDf, j, 'ema', feature_id)
        feature_id += 1

    Sample += '\n'
    problem_file.write(Sample)

    problem_file.close()


print __name__
'''
if __name__ == '__main__':
    #print sys.path
    print 'the argv is ', sys.argv, 'len is', len(sys.argv)
    for i in range(1,len(sys.argv)):
        print  "Argument",i,sys.argv[i]


    StockCode = sys.argv[1]
    Df = fetch_stock_data(StockCode)
    print Df[0]
    #genFeature(Df[0], Df[1])
'''
