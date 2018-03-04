# -*- coding: utf-8 -*-

import glob, csv, datetime
from sklearn.linear_model import LogisticRegression

def train_model():
    up_list = glob.glob("./csv/*up*.csv")
    down_list = glob.glob("./csv/*down*.csv")
    X = []
    y = []
    m = 10 # m的值为2-15
#    count = 0
    
    print('涨停模型训练:')    
    print('-- 涨停共有%s次数据'%(len(up_list)))

    for up_csv in up_list:
        with open(up_csv) as csv_file:
            lines = csv.reader(csv_file, delimiter=' ', quotechar='|')
            last_line = [[], [], []]
            
            for line in lines:
                line = line[0].split(',')
                up_limit = float(line[1]) * 100
                break
            
            for index,line in reversed(list(enumerate(lines))):
                if len(line) == 0:
                    continue
                elif len(line[0]) < 5:
                    continue
                
                line = line[0].split(',')
                x = [1] # X0
                
                delta_time = 0
                volume_1 = 0
                volume_2 = 0
                volume_3 = 0
                dist_1 = 0
                dist_1_indicate = 0
                if len(last_line[2]):
                    delta_time = (datetime.datetime.strptime(line[0],'%H:%M:%S') - datetime.datetime.strptime(last_line[2][0],'%H:%M:%S')).total_seconds()
                    volume_1 = int(last_line[2][3]) / 1000
                    dist_1 = up_limit - float(last_line[2][1]) * 100
                    if dist_1 < m:
                        dist_1_indicate = dist_1
                if len(last_line[1]):
                    volume_2 = int(last_line[1][3]) / 1000
                if len(last_line[0]):
                    volume_3 = int(last_line[0][3]) / 1000
                    
                last_line.pop(0)
                last_line.append(line)
                    
                x.append(delta_time) # X1
                x.append(volume_1) # X2
                x.append(volume_2) # X3
                x.append(volume_3) # X4
                x.append(dist_1) #X5
                x.append(dist_1_indicate) # X6
                x.append(0) # X7 set to zero when bid or ask price is not available
                x.append(1) # X8 set bid and ask price to change direction
                x.append(1) # X9
                x.append(0) # X10
                x.append(0) # X11
                x.append(0) # X12
                x.append(0) # X13
                x.append(0) # X14
                x.append(0) # X15
                x.append(0) # X16
                x.append(0) # X17
                x.append(0) # X18
                
                X.append(x)
                
                if line[2] != '--' and float(line[2]) > 0:
                    y.append(1)
                else:
                    y.append(0)
                
    print('-- 训练数据集大小:%s'%(len(y)))
    for example in X[1300:1320]: print(example)

    classifier = LogisticRegression()
    classifier.fit(X, y)
    print('-- 训练结果参数:%s'%(classifier.coef_))
    prediction = classifier.predict(X[1300:1320])
    print(y[1300:1320])
    print(prediction)

#    print('跌停共有%s次数据'%(len(down_list)))
    

# 训练逻辑回归模型
train_model()

