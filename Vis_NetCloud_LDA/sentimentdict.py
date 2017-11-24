# - * - coding:utf-8 - * - -

import os
os_path = 'sentiment/'

# 获取sentiment文件夹下所有文件的内容
def file_name(file_dir):
    filecontent = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if '.txt' in file:
                filecontent.append(file)
    return filecontent
filecontent = file_name('sentiment')

sentidict={'pos':[],'neg':[]}

# 读取文件内容
for file in filecontent:
    # 根据文件的名字判断该文件的信息是积极的还是消极的
    senti = file.split('_')[0]
    f = open(os_path+file,'r')
    content  = f.readlines()
    for i in content[2:]:
        sentidict[senti].append(i.strip('\r\n').strip().decode('gbk').encode('utf8'))

print 'Get Sentiment Dictionary Done!'