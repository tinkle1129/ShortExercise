# - * - coding:utf-8 - * - -
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
import pandas as pd
import jieba.analyse
import datetime
import getstopwords

print datetime.datetime.now()

stopwords = getstopwords.stopwords

def generateCloud(txtFreq,fontname,imagename,cloudname):

    #生成标签云的函数

    coloring = imread(imagename)             # 读取背景图片
    wc = WordCloud(background_color="white", # 背景颜色max_words=2000,# 词云显示的最大词数
                   mask=coloring,            # 设置背景图片
                   font_path=fontname,       # 兼容中文字体
                   max_font_size=100)        # 字体最大值

    #计算好词频后使用generate_from_frequencies函数生成词云
    wc.generate_from_frequencies(txtFreq)
    # 生成图片
    plt.imshow(wc)
    plt.axis("off")
    # 绘制词云
    plt.figure()
    # 保存词云
    wc.to_file(cloudname)

# 读取数据
df = pd.read_csv('data/comments.csv')

singers = list(set(df['singer']))

top10singers=[]
for singer in singers:
    top10singers.append((singer,len(df[df['singer']==singer]['song'].value_counts()))) #统计歌手入选曲目数量
sortedtop10=sorted(top10singers,key=lambda x:x[1],reverse=True)[0:10]

for i in sortedtop10:
    singer = i[0]
    content = ' '.join(df['comment'][df['singer']==singer].tolist())
    final = ''
    for token in content.split():   # 去除停用词
        if token not in stopwords:
                final += ' '+token
    top10comments = jieba.analyse.extract_tags(final, topK=50, withWeight=True, allowPOS=())
    txtFreq = {}
    for key in top10comments:
        txtFreq[key[0]] = key[1] #改写成字典的形式
    generateCloud(txtFreq, 'hanyu.ttf', 'circle.png', 'displays/'+singer+'.png')

print datetime.datetime.now() #大约三分钟
