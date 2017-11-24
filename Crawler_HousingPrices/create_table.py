# -*- coding:utf-8 -*-  
import MySQLdb
import re
#housingprice
class Database:
    def __init__(self):
        self.conn = MySQLdb.connect(
            user='root',passwd='123456',
            db = 'hp',charset='utf8',
        )
    def create_list(self):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            #msg_id, name, state, price, address_1, address_2, address_3, huxing, square, price * square
            cur.execute('create table datalist(ID INT, NAME TEXT, STATE TEXT, PRICE FLOAT, address_1 TEXT, address_2 TEXT, address_3 TEXT,'
                        'huxing TEXT, square float, totalprice float,primaryID BIGINT,type int(5),PRIMARY KEY (primaryID))default charset=utf8')
    def insertdata(self,data,t):
        with self.conn:
            primaryID=int(data[0]+''.join(re.findall('[0-9]',data[7]))+''.join(re.findall('[0-9]',str(data[8]))))
            print primaryID
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = 'insert ignore into datalist(ID,NAME,STATE,PRICE,address_1,address_2,address_3,huxing,square,totalprice,primaryID,type) values(%d,"%s","%s",%f,"%s","%s","%s","%s",%f,"%s",%d,%d)'\
                  %(int(data[0]),data[1].encode('utf8'),data[2].encode('utf8'),data[3],data[4].encode('utf8'),data[5].encode('utf8'),data[6].encode('utf8'),data[7].encode('utf8'),data[8],data[9],primaryID,t)
            cur.execute(sql)
            self.conn.commit()
    def setgbk(self):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = 'set names gbk'
            cur.execute(sql)
            self.conn.commit()
    def getdetails(self,sql):
        with self.conn:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql)
            info = cur.fetchall()
            return info

'''
S = Database()
S.create_list()
data = (u'263892', u'\u4e1c\u6da6\u57ce', u'\uff0843\u6761\u70b9\u8bc4\uff09', 12000.0, u'\u90d1\u4e1c\u65b0\u533a', u'\u90d1\u4e1c\u65b0\u533a', u'\u5546\u90fd\u8def\u4e0e\u524d\u7a0b\u8def\u4ea4\u53c9\u53e3\u4e1c1000\u7c73', u'3\u5ba42\u53852\u536b', 125.0, 1500000.0)
S.insertdata(data,1)
'''