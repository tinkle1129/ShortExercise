
# -*- coding:utf-8 -*-  
import subprocess
import create_table
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
S = create_table.Database()
#df = S.getmsg()

PROMPT_STR = '\n1:房屋信息检索\n2:房屋信息描述\n其他:退出系统\n请输入你的选项'
STR = '\n 1:户型信息检索\n2:小区名称信息检索\n其他：退出子系统\n'
def gethuxing():
    huxing=[]
    info = S.getdetails('select huxing,count(*) from datalist group by huxing')
    for i in info:
        huxing.append((i['huxing'],i['count(*)']))
    return huxing

def getNAME():
    name = []
    info = S.getdetails('select NAME,count(*) from datalist group by NAME')
    for i in info:
        name.append((i['NAME'],i['count(*)']))
    return name

def getaddress_1():
    address_1 = []
    info = S.getdetails('select address_1,count(*) from datalist group by address_1')
    for i in info:
        address_1.append((i['address_1'],i['count(*)']))
    return address_1

def getaddress_2(addr1):
    address_2 = []
    info = S.getdetails('select address_2,count(*) from datalist where address_1 = "%s "group by address_2' % addr1)
    for i in info:
        address_2.append((i['address_2'],i['count(*)']))
    return address_2

huxing = gethuxing()
address_1 = getaddress_1()
name = getNAME()

def show(msg,strname):
    print ' 你查询的是: '
    print strname
    print ' 共有数量： '
    print len(msg)
    c =''
    while(c.strip() not in ['Y','y','n','N']):
        print '\n是否全部显示'
        c = raw_input('(Y/N)? \n')
    if c.strip() in ['Y','y']:
        print '      '+strname+'      |        个数      '
        for line in msg:
            print ' '+line[0].encode('utf8').strip()+(20-len(line[0].strip()))*' '+'  '+str(line[1])

def monitor():
    subprocess.call("cls",shell=True)
    print '#--------------------------------------------------#'
    print '#             郑州市房地产信息查询                 #'
    print '#             制作：XXX                            #'
    print '#--------------------------------------------------#'
def query():
    def querytype():
        monitor()
        print ' 请选择要查询的房源类型 1:新房 2:二手房 3:新房或者二手房 其他:退出操作\n'
        housetype = raw_input()
        if housetype.strip()=='1':
            return 1
        elif housetype.strip()=='2':
            return 2
        elif  housetype.strip()=='3':
            return 0
        else:
            return -1
    def querystate():
        monitor()
        print ' 请选择查看新房当前销售情况的类型 1:在售 2:待售 3:售罄 4:推荐 5:全部 其他:退出操作\n'
        state = raw_input()
        if state.strip()=='1':
            return u'在售'
        elif state.strip()=='2':
            return u'待售'
        elif  state.strip()=='3':
            return u'售罄'
        elif state.strip()=='4':
            return u'推荐'
        elif state.strip()=='5':
            return 0
        else:
            return -1
    def queryarea(address):
        monitor()
        print ' 请选择查看区域'
        print ' 0: 全部'
        for idx,item in enumerate(address):
            print idx+1,' '+item[0].encode('utf8')
        area = raw_input()
        try:
            area=int(area.strip())-1
            if area==-1:
                return 0
            else:
                return address[area][0]
        except:
            return -1
    def queryhuxing():
        monitor()
        print ' 请选择查看户型'
        print ' 0: 全部'
        for idx,item in enumerate(huxing):
            print idx+1,' '+item[0].encode('utf8')
        area = raw_input()
        try:
            area=int(area.strip())-1
            if area==-1:
                return 0
            else:
                return huxing[area][0]
        except:
            return -1
    def querypricearea():
        monitor()
        print ' 请输入单位面积价格区间'
        flag = 1
        while(flag):
            lowprice=raw_input(' 请输入最小范围，如果不设置用小于等于0的数字代替\n')
            try:
                lowprice=float(lowprice.strip())
                if lowprice<0:
                    lowprice=0
                flag=0
            except:
                pass
        flag = 1
        while(flag):
            highprice=raw_input(' 请输入最大范围，如果不设置用小于等于0的数字代替\n')
            try:
                highprice=float(highprice.strip())
                if highprice<=0:
                    highprice=-1
                flag=0
            except:
                pass
        return (lowprice,highprice)

    housetype=querytype()
    if housetype==1:
        state = querystate()
    else:
        state=0
    adr_1 = queryarea(address_1)
    if adr_1!=0 and adr_1!=-1:
        address_2 = getaddress_2(adr_1)
        adr_2 = queryarea(address_2)
    else:
        adr_2 = 0
    hx = queryhuxing()
    priceRange= querypricearea()
    areaRange = querypricearea()
    sql = 'select * from datalist '
    def checkflag(flag,sql):
        if flag:
            flag=0
            sql = sql + ' where '
        else:
            sql = sql + ' and '
        return flag,sql
    flag = 1
    if housetype==1 or housetype==2:
        flag,sql = checkflag(flag,sql)
        sql = sql + ' type='+str(housetype)
    if state!=0 and state!=-1:
        flag,sql = checkflag(flag,sql)
        sql = sql + ' STATE="%s"' %state
    if adr_1!=0 and adr_1!=-1:
        flag,sql = checkflag(flag,sql)
        sql = sql + ' address_1="%s"' %adr_1
    if adr_2!=0 and adr_2!=-1:
        flag,sql = checkflag(flag,sql)
        sql = sql + ' address_2="%s"' %adr_2
    if hx!=0 and hx!=-1:
        flag,sql = checkflag(flag,sql)
        sql = sql + ' huxing="%s"' %hx
    flag, sql = checkflag(flag, sql)
    sql = sql + 'price>=%f' %priceRange[0]
    if priceRange[1]>0:
        flag, sql = checkflag(flag, sql)
        sql = sql + 'price<=%f' % priceRange[1]
    flag, sql = checkflag(flag, sql)
    sql = sql + 'square>=%f' %areaRange[0]
    if areaRange[1]>0:
        flag, sql = checkflag(flag, sql)
        sql = sql + 'square<=%f' % areaRange[1]
    print sql.encode('utf8')
    info = S.getdetails(sql)
    #print '          小区名称       | 当前状态 | 单位面积价格|address_1|address_2|address_3            |          户型       | 面积| 总价| 类型'
    for i in info:
        ht = i['type']
        if ht == 1:
            ht = '新房'
        else:
            ht = '二手房'
        print ' '+i['NAME'].encode('utf8')+' '+i['STATE'].encode('utf8')+' '+str(i['PRICE'])+' '+i['address_1'].encode('utf8')+' '+i['address_2'].encode('utf8')+' '+i['address_3'].encode('utf8')+' '+i['huxing'].encode('utf8')+' '+str(i['square'])+' '+str(i['totalprice'])+' '+ht
    print ' 共有 '+str(len(info))+' 条信息'

def main():
    monitor()
    print PROMPT_STR
    choice = raw_input()
    flag = 1
    while(flag):

        if choice.strip()=='1':
            query()
            os.system("pause")
            monitor()
            print PROMPT_STR
            choice = raw_input()
        elif choice.strip()=='2':
            monitor()
            c2 = raw_input(STR)
            if c2.strip()=='1':
                show(huxing,' 户型')
                os.system("pause")
            elif c2.strip()=='2':
                show(name,' 小区名称')
                os.system("pause")
            else:
                monitor()
                print PROMPT_STR
                choice = raw_input()
        else:
            monitor()
            print '#             欢迎下次使用本系统                   #'
            print '#--------------------------------------------------#'
            flag = 0

if __name__ == '__main__':

    main()






