import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
def extract_tags(content,topk):
    content = content.strip()
    tags=jieba.analyse.extract_tags(content, topK=topk)
    return tags

f = open('data/train2.dat','r')
content = f.readlines()
tmp =[]
ret = []
for line in content:
    tmp.extend(extract_tags(line.strip('\n'),50))
for t in tmp:
    if t not in ret and tmp.count(t)>1:
        ret.append(t)

plt.figure()
wc = WordCloud(background_color="white").generate(' '.join(ret))
plt.imshow(wc)
plt.show()