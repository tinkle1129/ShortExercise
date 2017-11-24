import pandas as pd
import numpy as np
import settings
import datetime
import matplotlib.pyplot as plt

DF = pd.read_csv('data/attitude.csv')
# Intialization
DF['ATTITUDE']=[0.0 for i in range(len(DF))]


data = pd.read_csv('twitter_message_official.csv')
def trans(date_x):
    return datetime.datetime.strptime(date_x, '%Y-%m-%dT%H:%M:%S')
data['created_at']=data['created_at'].map(trans)
for l in set(data['user_loc']):
    Messages = zip(data['created_at'][data['user_loc'] == l], data['p_pos'][data['user_loc'] == l])
    v=sorted(Messages,key=lambda x:x[0],reverse=True)[0]
    for i in range(len(DF)):
        if DF['CODE'][i]==l:
            DF['ATTITUDE'][i]=v[1]
    print l,v
'''
for l in settings.OFFICIAL_LOC:
    msg = np.array(data['p_pos'][data['user_loc']==l])
    pos = msg[msg>0.5]
    neg = msg[msg<=0.5]
    if len(pos)<len(neg):
        v = np.mean(neg)
    elif len(pos)>len(neg):
        v = np.mean(pos)
    else:
        v = np.mean(msg)
    for i in range(len(DF)):
        if DF['CODE'][i]==l:
            DF['ATTITUDE'][i]=v
'''

DF.to_csv('data/attitude.csv', index=False)
