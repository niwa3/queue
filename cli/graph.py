# !/usr/bin/python3
# coding: UTF-8
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    names = [i for i in range(1000247)]
    data = pd.read_csv('./input1705.csv', names=names, index_col=0)
    # data = pd.read_csv('./input1705.csv', header=0, index_col=0)
    print(data.head())
    '''
    tags = [
        'q0', 'q1', 'q2', 'q3', 'q4',
        'q5', 'q6', 'q7', 'q8', 'q9',
        'q10', 'q11', 'q12', 'q13', 'q14',
        'q15', 'q16', 'q17', 'q18', 'q19'
    ]
    '''
    tags = data.index

    plt.figure()
    '''
    for i in tags:
        qIn = data.loc[i].round(2)
        ps = []
        flag = 0
        j = 0
        while j < int(np.round(qIn.max())):
            tmp = 0
            if qIn[flag] > j+10:
                ps.append(0)
                j += 10
                continue
            tmp = (qIn[flag:] <= j+10).sum()
            tmp = 0 if tmp is None else tmp
            ps.append(tmp)
            flag += tmp
            j += 10
        ps = pd.Series(ps)
        ps.value_counts().sort_index().plot()
    '''
    for i in tags:
        qIn = pd.Series(np.floor(data.loc[i]))
        qCount = qIn.value_counts()
        pro = pd.Series([qIn.max()-qIn.min()-len(qCount)]
                        ).append(qCount.value_counts())
        pro.plot()
    plt.savefig('arrivalProcess.png')
    plt.close('all')
