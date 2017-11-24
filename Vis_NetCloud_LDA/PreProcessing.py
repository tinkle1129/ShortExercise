# - * - coding:utf-8 - * - -

import pandas as pd
import re
from sentimentdict import sentidict
from datetime import datetime
import getstopwords
stopwords = getstopwords.stopwords

def cleanData():
    f = open('data/comments.xls')
    content = f.readlines()
    song = []
    singer = []
    ID = []
    comment = []
    thumbsup = []
    tmpline = []
    for line in content:
        line = tmpline + (line.strip('\n').strip('\t').split('\t'))
        try:
            int(line[-1])
            temp = line[2:-2][0].decode("utf8")
            #过滤一些奇奇怪怪的标点符号
            filter_ = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), temp)
            comment.append(filter_.encode("utf8"))
            thumbsup.append(int(line[-1]))
            song.append(line[0])
            singer.append(line[1])
            ID.append(line[-2])
            tmpline = []
        except:
            tmpline = line

    dict_ = {'singer':singer,'song':song,'ID':ID,'comment':comment,'thumbsup':thumbsup}
    df = pd.DataFrame(dict_,columns=['singer','song','thumbsup','comment','ID'])

    thread = sorted(df['thumbsup'].tolist(),reverse=True)[50000]
    df = df[df['thumbsup']>=thread] #选取前50000条热门评论

    df.to_csv('data/comments.csv',index=None)
    print 'Clean Data Done, result saved in data/comments.csv now, which includes %s data' % len(df)

cleanData()

# 读取数据
df = pd.read_csv('data/comments.csv')



# 获取情感分值内容
import thulac
thul = thulac.thulac(seg_only=True)

def getsentiscore(text):
    if isinstance(text,float):  #存在有些情况下数据是nan的情况
        return 0.0

    text = thul.cut(text, text=True)    # 分词

    final = ''
    for token in text.split():   # 去除停用词
        if token not in stopwords:
                final += ' '+token
    seg_list = thul.cut(final, text=True)

    pos = 0
    neg = 0
    for seg in seg_list.split():
        if seg in sentidict['pos']:
            pos +=1
        if seg in sentidict['neg']:
            neg +=1

    if len(seg_list.split())==0:
        return 0.0
    else:
        return float(pos-neg)/len(seg_list.split())

print len(df)

sentiscore = []
print datetime.now()
for idx in range(len(df['comment'])):
    if idx%1000==0:
        print datetime.now()  # 因为这个要执行好久，所以每1000个打印一下
        print idx
    try:
        sentiscore.append(getsentiscore(df['comment'][idx]))
    except:
        sentiscore.append(0)

df['sentiscore'] = sentiscore
df.to_csv('data/comments.csv',index=None)
