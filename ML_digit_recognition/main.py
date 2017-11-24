# -*-- coding = utf-8 --*-
import preprocessing
#preprocessing.convert_data()
import svmmodel
import numpy as np

ans,ret = preprocessing.convert_input('recog')

# save data
result = open('data/result.txt','w')
for idx in [0.001,0.003,0.005,0.007,0.009,
            0.01,0.03,0.05,0.07,0.09,
            0.1,0.3,0.5,0.7,0.8,0.9,1]:
    clf,acc = svmmodel.getAccuraty(idx)
    result.write(str(idx)+' '+str(acc)+'\n')
    for i in range(len(ans)):
        out = ''
        for inst in ret[i]:
            inst = np.array(inst).reshape((1, 27))
            predict = clf.predict(inst)
            out = out + str(predict[0])
        print(ans[i], out)
result.close()



