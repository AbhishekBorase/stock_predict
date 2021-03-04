import pandas as pd
import pandas_datareader as web
import numpy as np
from sklearn.svm import SVR

import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
from datetime import datetime


def model(symbol, e, s='2015-01-01'):
    df = web.DataReader(symbol, data_source='yahoo', start=s, end=e)

    close = df['Adj Close']
    prev_close = [np.nan]
    for i in close:
        prev_close.append(i)
    prev_close.pop()
    df['prev_Close'] = prev_close

    df = df.drop(['High', 'Low', 'Volume', 'Close', 'Open'], axis=1)

    df['date'] = df.index.strftime("%Y-%m-%d")

    df = df.dropna()

    df_adj_close = list(df.loc[:, 'Adj Close'])
    X = []
    i = 0
    for j in df['prev_Close']:
        X.append([i, j])
        i += 1

    days = []
    for i in range(len(X)):
        days.append([i])

    rbf_svr = SVR(kernel='rbf', C=10000.0, gamma=0.00000001)
    rbf_svr.fit(X, df_adj_close)

    dayG = [[X[-1][0] + 1]]
    day = [[X[-1][0] + 1, df.iloc[-1]['Adj Close']]]

    pred = {'Adj Close': rbf_svr.predict(day)[0], 'prev_Close': day[0][-1], 'date': datetime.now}

    df = df.append(pred, ignore_index=True)

    for i in range(10, 210, 10):
        df[f'MA_{i}'] = df.iloc[:, 1].rolling(window=i).mean()

    df = df.dropna()
    return df


def buy_sell_short(df, flag=0):
    buy = []
    sell = []
    predict = df.tail(1)
    today = df.tail(2).head(1)


    ma_30 = predict.iloc[0]['MA_30']
    ma_10 = predict.iloc[0]['MA_10']
    t_30 = today.iloc[0]['MA_30']
    t_10 = today.iloc[0]['MA_10']
    if flag == -1:
        if predict.iloc[0]['MA_70'] < ma_30 and ma_30 < ma_10 and t_10 >= t_30:
            print('BUY')
            buy.append([predict.index[0] - 1, predict.iloc[0]['Adj Close']])
            flag = 1
    elif flag == 1:

        if predict.iloc[0]['MA_70'] > ma_30 or ma_30 > ma_10 or t_10 <= t_30:
            print('SELL')
            sell.append([predict.index[0] - 1, predict.iloc[0]['Adj Close']])
            flag = -1
    elif flag == 0:
        if predict.iloc[0]['MA_70'] < ma_30 < ma_10 and t_30 <= t_10:
            if ((ma_10 - ma_30) / ma_10) * 100 <= 1 and ma_10 >= t_10 and ma_30 >= t_30:
                print('BUY')
                buy.append([predict.index[0] - 1, predict.iloc[0]['Adj Close']])
                flag = 1

    return buy, sell, flag
