# - * - coding:utf-8 - * - -
def loadstopwords():
    f = open('data/stopwords.txt')
    stopwords = f.readlines()
    return list(map(lambda x:x.strip('\r\n'),stopwords))
stopwords = loadstopwords()