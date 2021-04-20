import os
import time
import numpy as np

def writeFile(filepath,content):
    with open(filepath,'w') as f:
        f.write(str(content))
    
def readFile(filepath):
    with open(filepath) as f:
        content = f.read()
    return content.splitlines()

if __name__ == '__main__':
    n = 40

    # learn
    time_train = []
    for i in range(n):
        tmp = readFile('../data/cross_data_py/%s/time-train'%i)[0]
        time_train.append(eval(tmp))

    # predict
    time_predict = []
    for i in range(n):
        tmp = readFile('../data/cross_data_py/%s/time-predict'%i)[0]
        time_predict.append(eval(tmp))
    
    print(np.mean(time_train))
    print(np.max(time_train))
    print(np.min(time_train))
    print(np.std(time_train,ddof=1))
    print('********************************')
    print(np.mean(time_predict))
    print(np.max(time_predict))
    print(np.min(time_predict))
    print(np.std(time_predict,ddof=1))