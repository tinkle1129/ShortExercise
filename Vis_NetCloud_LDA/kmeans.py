# - * - coding:utf-8 - * - -
import re
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
transformer = TfidfTransformer()

f_handle = open('displays/song_lda.txt','r')
contents = f_handle.readlines()
corpus = []
singers = {}
singer = ''

for line in contents:
    if len(line.strip('\n')):
        if '*==========================*' in line:
            singer = line.strip('\n').strip('*==========================*')
        elif '=' not in line:
            corpus.append(' '.join(re.findall('\"(.*?)\"',line.strip('\n'))))
            singers.setdefault(len(corpus)-1,singer)

print 'The number of lda topics is %s ' % len(corpus)

tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
word = vectorizer.get_feature_names()
weight = tfidf.toarray()

k = 50 # Param: Define the number of clusters

clf = KMeans(n_clusters=k)
s = clf.fit(weight)

kmeansdict ={}
kmeanssinger = {}
for i in range(len(corpus)):
    kmeansdict.setdefault(clf.labels_[i],[])
    kmeansdict[clf.labels_[i]].extend(corpus[i].split())
    kmeanssinger.setdefault(clf.labels_[i],[])
    kmeanssinger[clf.labels_[i]].append(singers[i])

for i in range(k):
    print '==========================='
    print 'The %s classify' % i
    print '==========================='
    print 'singers:' +  ' '.join(list(set(kmeanssinger[i])))
    print ' '.join(list(set(kmeansdict[i])))