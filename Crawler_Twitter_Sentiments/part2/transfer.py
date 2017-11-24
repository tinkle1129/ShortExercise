def clean(doc):
    stopwords = {}.fromkeys([line.rstrip() for line in open('data/stopwords.txt')])
    normalized = " ".join(ch for ch in doc.lower().split() if ch not in stopwords)
    return normalized

f = open('data/train2.dat','r')
f_handle = open('data/train.dat','w')
content = f.readlines()
tmp =[]
ret = []
for line in content:
    f_handle.write(clean(line.strip('\n'))+'\n')
f_handle.close()