import urllib2
from bs4 import BeautifulSoup
import json
lc = ['cnn','YonhapNews']
keyword='thaad'
content = {}

for l in lc:
    querylist=l+'+'+keyword
    for i in range(20):
        url = 'https://www.google.com/search?q='+querylist+'&start='+str(i*10)
        print url
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url,headers=headers)
        data = urllib2.urlopen(req).read()
        soup = BeautifulSoup(data,'lxml')
        for link in soup.find_all('a'):
            if 'http' in link.get('href'):
                if '/url?q=' in link.get('href'):
                    content.setdefault(l,[])
                    content[l].append(link.get('href').strip('/url?q='))
with open('data/newsdata.json', 'w') as json_file:
    json_file.write(json.dumps(content))
