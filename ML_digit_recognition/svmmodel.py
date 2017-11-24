# -*-- coding = utf-8 --*-
import pprint, pickle
import numpy as np
import pandas as pd
from sklearn.svm import SVC
import random

# Load pickle
pkl_file = open('data/train.pkl', 'rb')
train_data = pickle.load(pkl_file)
pkl_file.close()

# change array into dataframe
name = []
for i in range(27):
    name.append(str(i))
name += ['label']


df_train = pd.DataFrame(train_data,columns=name)

print (df_train.head())

# get dummpy variables

dummy = pd.get_dummies(df_train['label']).rename(columns=lambda x: 'label_'+str(x))

df_train = pd.concat([df_train,dummy],axis=1)

pkl_file = open('data/test.pkl', 'rb')
test_data = pickle.load(pkl_file)
pkl_file.close()

df_test = pd.DataFrame(test_data, columns=name)

print(df_train.head())

def getAccuraty(rate):
    rate_df_train = df_train.ix[random.sample(range(len(df_train)), int(len(df_train)*rate)), :]
    X = rate_df_train[rate_df_train.columns[0 : 27]].values.tolist()

    Y = rate_df_train['label'].values.tolist()

    clf = SVC(decision_function_shape='ovo')

    clf.fit(X, Y)


    count = 0
    ans = []
    for i in range(len(df_test['label'])):
        inst = df_test[df_test.columns[0:27]].iloc[i].values.tolist()
        inst = np.array(inst).reshape((1,27))
        predict = clf.predict(inst)
        #print(predict, df_test['label'][i])
        if predict[0] == df_test['label'][i]:
            count += 1

    print('Accuracy Rate is :%f' %(float(count)/len(df_test['label'])))
    return clf,float(count)/len(df_test['label'])
