import json
from bs4 import BeautifulSoup
import urllib2
import re
import threading
import Queue
queue = Queue.Queue()
f = open('data/train2.dat','w')

class ThreadUrl(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            def clear(url):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                req = urllib2.Request(url, headers=headers)
                data = urllib2.urlopen(req).read()
                soup = BeautifulSoup(data, 'lxml')
                [script.extract() for script in soup.findAll('script')]
                [style.extract() for style in soup.findAll('style')]
                soup.prettify()
                reg1 = re.compile("<[^>]*>")
                content = reg1.sub('', soup.prettify())
                ret = []
                for i in content.split('\n'):
                    if len(i.split()) > 10:
                        ret.append(' '.join(i.split()))
                f.write(' '.join(ret).encode('utf8') + '\n')
            try:
                clear(url)
            except:
                pass
            print url
            self.queue.task_done()

def load():
    with open('data/newsdata.json') as json_file:
        data = json.load(json_file)
        return data

data = load()

def clear(url):
    print url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url, headers=headers)
    data = urllib2.urlopen(req).read()
    soup = BeautifulSoup(data,'lxml')
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    reg1 = re.compile("<[^>]*>")
    content = reg1.sub('', soup.prettify())
    ret = []
    for i in content.split('\n'):
        if len(i.split()) >10:
            ret.append(' '.join(i.split()))
    print 'ok!'
    return ' '.join(ret)

def main():
    msg = []
    for i in data.keys():
        msg.extend(data[i])

    for i in range(10):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    for m in msg:
        queue.put(m)

    queue.join()
main()
f.close()
'''
f = open('data/train2.dat','w')
for k in data.keys():
    doc_complete=[]
    for x in range(len(data[k])):
        try:
            c = clear(data[k][x])
            doc_complete.append(c)
        except:
            pass
    for con in doc_complete:
        f.write(con.encode('utf8')+'\n')
f.close()
'''