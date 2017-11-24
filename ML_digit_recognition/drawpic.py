# -*-- coding = utf-8 --*-
import matplotlib.pyplot as plt
import preprocessing

os_path = 'showunit/'
file_path = os_path+'3652.bmp'
bim = preprocessing.convertimg(file_path)
bim.save(os_path+'out.bmp')
child_imgs=preprocessing.get_crop_imgs(bim)
for idx in range(4):
    child_imgs[idx].save(os_path+'out_'+str(idx)+'.bmp')

f = open('data/result.txt','r')
content = f.readlines()
x = []
y = []
for line in content:
    x.append(float(line.strip('\n').split(' ')[0]))
    y.append(float(line.strip('\n').split(' ')[1]))
plt.figure()
plt.plot(x,y,'r-')
plt.xlabel('Train Data Sample Rate')
plt.ylabel('Accuracy Rate')
plt.grid()
plt.savefig('showunit/accuracy.jpg')