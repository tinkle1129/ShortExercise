# -*- coding:utf-8 -*-  
import urllib2
from bs4 import BeautifulSoup
import re
from datetime import datetime
import Queue
import threading
import sys
import create_table
import time
queue = Queue.Queue()
out_queue = Queue.Queue()


S = create_table.Database()
#S.create_list()
class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
    method.
    Come from:
    Kill a thread in Python:
    http://mail.python.org/pipermail/python-list/2004-May/260937.html
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)
    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None
    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace
    def kill(self):
        self.killed = True
class Timeout(Exception):
    """function run timeout"""
def timeout(seconds):
    def timeout_decorator(func):
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                #print 'Time Out!'
                return -1
            else:
                return result
        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _
    return timeout_decorator

class ThreadUrl(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_que = out_queue

    def run(self):
        while True:
            test = self.queue.get()
            msg_id, name, state, price, address_1, address_2, address_3,page = test[0], test[1], test[2], test[3], test[4], \
                                                                          test[5], test[6],test[7]
            #print msg_id
            huxingUrl = 'http://zz.fang.anjuke.com/loupan/huxing-' + msg_id + '/s?p=' + str(page)
            #print huxingUrl

            @timeout(20)
            def getmessage(huxingUrl,test):
                ret = []
                msg_id, name, state, price, address_1, address_2, address_3, page = test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7]
                res = urllib2.urlopen(huxingUrl)
                soup = BeautifulSoup(res, 'lxml')
                for listall in soup.find_all('div', 'hx-list-mod'):
                    if listall.text.strip('\n') != '':
                        for link in listall.find_all('div', 'type-name'):
                            huxing = link.find(class_='desc-txt').text.strip('\n').split('\n')[-1]
                            square = float(re.findall('[0-9]*\.[0-9]*', link.find(class_='desc-k area-k').text)[0])
                            ret.append((msg_id.strip(), name.strip(), state.strip(), price, address_1.strip(), address_2.strip(), address_3.strip(), huxing.strip(), square, price * square))
                return ret
            res=getmessage(huxingUrl,test)
            if res == -1:
                self.queue.put(test)
            else:
                for data in res:
                    self.out_que.put(data)

            self.queue.task_done()

class DatamineThread(threading.Thread):
    def __init__(self,out_queue,t):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        self.t = t
    def run(self):
        while True:
            data = self.out_queue.get()
            for d in data:
                S.insertdata(d,self.t)
            #print data
            self.out_queue.task_done()

def getNewMSG():
    page = 1
    flag=1
    content =[]
    while(flag and page<=17):
        url = 'http://zz.fang.anjuke.com/loupan/all/p'+str(page)+'/'
        print url
        res = urllib2.urlopen(url)
        #content = res.read().decode('utf-8')
        soup = BeautifulSoup(res,'html5lib') #lxml
        flag =1
        for listall in soup.find_all('div','key-list'):
            if listall.text.strip('\n')=='':
                flag =0
            for link in listall.find_all('div','item-mod'):
                msg = link.find(class_='lp-name').text.strip('\n').split('\n')
                msg_id = re.findall('[0-9]+',link.find(class_='lp-name').find(class_='items-name').get('href'))[0]
                name = msg[0].strip()
                state = msg[1].strip()
                adr = link.find(class_='address').text.strip('\n').split(u'\xa0')
                address_1 = adr[1]
                address_2 = adr[2]
                address_3 = adr[-1]
                try:
                    price = float(re.findall('[0-9]+',link.find(class_='price').text)[0])
                except:
                    price = -1
                for i in range(1,3):
                    content.append([msg_id,name,state,price,address_1,address_2,address_3,i])
        page = page +1
    return content

def main():
    print 'Start new Housing'
    content = getNewMSG()
    #print len(content)
    for i in range(10):
        t = ThreadUrl(queue,out_queue)
        t.setDaemon(True)
        t.start()
    for host in content:
        queue.put(host)

    for j in range(1):
        dt = DatamineThread(out_queue,1)
        dt.setDaemon(True)
        dt.start()

    queue.join()
    out_queue.join()

def secmain():
    def getmessage(url):
        ret = []
        req = urllib2.Request(url)
        print url
        req.add_header('Referer', url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        res = urllib2.urlopen(req)
        soup = BeautifulSoup(res, 'lxml')  # lxml
        print res.read()
        for listall in soup.find_all('div', 'house-details'):
            msg = listall.find(class_='details-item').text.split('|')
            square = float(re.findall('[0-9]+', msg[1].encode('utf8'))[0])
            huxing = msg[0]
            price = float(re.findall('[0-9]+', msg[2])[0])
            address = listall.find(class_='comm-address').text.strip('\n').split('\n')
            name = address[0].strip()
            sedaddr = address[1].strip().split(u'\xa0')
            address_1 = sedaddr[0].split('-')[0]
            address_2 = sedaddr[0].split('-')[1]
            address_3 = sedaddr[0].split('-')[2]#sedaddr[1][:-1]
            href = listall.find(class_='houseListTitle').get("href")
            msg_id = re.findall('[0-9]+', href)[0]
            state = '0'
            ret.append(
                [msg_id.strip(), name.strip(), state.strip(), price, address_1.strip(), address_2.strip(),
                 address_3.strip(), huxing.strip(), square, price * square])
        i = 0
        for listall in soup.find_all('div','pro-price'):
            price= float(re.findall('[0-9]+', listall.find(class_='unit-price').text)[0])
            ret[i][3]=price
            ret[i][-1]=price*ret[i][-2]
            i = i+1
        return ret

    for i in range(1,51):
        url='http://zhengzhou.anjuke.com/sale/p'+str(i)
        data = getmessage(url)
        for d in data:
            S.insertdata(d, 2)

if  __name__ == '__main__':
    #print datetime.now()
    #main()
    print datetime.now()
    secmain()
