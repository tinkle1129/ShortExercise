# - * - coding:utf-8 - * - -
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

comments = pd.read_csv('data/comments.csv')

singers = []
num_song = []
meanthumb = []
meansenti = []
print comments.head()
for singer in set(comments['singer']):
    if isinstance(singer,str):
        singers.append(singer)
        num_song.append(len(comments['song'][comments['singer']==singer].value_counts()))
        meanthumb.append(np.mean(list(comments['thumbsup'][comments['singer']==singer])))
        meansenti.append(np.mean(list(comments['sentiscore'][comments['singer'] == singer])))

data = pd.DataFrame()
data['singer'] = singers
data['num_song'] = num_song
data['meanthumb'] = meanthumb
data['meansenti'] = meansenti
data['meanthumb'].plot()
plt.ylabel(u'平均点赞数')
plt.savefig('displays/meanthumb.jpg')

plt.figure()
data['meansenti'].plot()
plt.ylabel(u'平均情感分')
plt.savefig('displays/meansenti.jpg')
data.to_csv('data/stats.csv',index=False)
