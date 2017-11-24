# - * - coding:utf-8 - * - -
import pandas as pd
from gensim import corpora,similarities
from gensim.models import LdaModel


def loadstopwords():
    f = open('data/stopwords.txt')
    stopwords = f.readlines()
    return list(map(lambda x:x.strip('\r\n'),stopwords))
stopwords = loadstopwords()

import thulac

thul = thulac.thulac(seg_only=True)
def cutwords(text):

    if isinstance(text,float):  #存在有些情况下数据是nan的情况
            return ' '
    text = thul.cut(text, text=True)    # 分词

    final = ''
    for token in text.split():   # 去除停用词
        if token not in stopwords:
            final += ' '+token
    seg_list = thul.cut(final, text=True)
    return seg_list.strip().split()

def lda_filter(documents):
    texts = [cutwords(doc) for doc in documents]
    dict = corpora.Dictionary(texts)    #自建词典
    #通过dict将用字符串表示的文档转换为用id表示的文档向量
    corpus = [dict.doc2bow(text) for text in texts]
    lda = LdaModel(corpus=corpus, id2word=dict, num_topics=10)
    return lda.print_topic(0)

# 读取数据
df = pd.read_csv('data/comments.csv')
print df.head()

singers = list(set(df['singer']))

top10singers=[]
for singer in singers:
    top10singers.append((singer,len(df[df['singer']==singer]['song'].value_counts()))) #统计歌手入选曲目数量
sortedtop10=sorted(top10singers,key=lambda x:x[1],reverse=True)[0:10]


f = open('displays/song_lda.txt','w')
for singer in sortedtop10:
    f.write('*==========================*')
    f.write('%s\n' %singer[0])

    songlist = list(set(df['song'][df['singer']==singer[0]]))
    for song in songlist:
        f.write('==========================')
        f.write('%s\n' % song)
        try:
            documents = df['comment'][(df['song']==song)&(df['singer']==singer[0])]
            topic = lda_filter(documents)
            f.write('%s\n' % topic.encode('utf8'))
        except:
            print singer[0]

    f.write('\n\n\n\n')
f.close()
