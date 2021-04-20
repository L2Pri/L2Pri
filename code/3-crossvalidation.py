import os
import time

def writeFile(filepath,content):
    with open(filepath,'w') as f:
        f.write(str(content))

if __name__ == '__main__':
    n = 40

    # learn
    for i in range(n):
        st_time = time.time()
        os.system('svm_rank/svm_rank_learn -c 1 data/cross_data_py/%s/train.dat data/cross_data_py/%s/svmrank-model.dat'%(i,i))
        en_time = time.time()
        tmp_train = en_time*1000 - st_time*1000
        print('***********************************************')
        print('training time is %s'%tmp_train)
        print('***********************************************')
        writeFile('data/cross_data_py/%s/time-train'%i,tmp_train)

    # predict
    for i in range(n):
        st_time = time.time()
        os.system('svm_rank/svm_rank_classify data/cross_data_py/%s/test.dat data/cross_data_py/%s/svmrank-model.dat data/cross_data_py/%s/svmrank-pred.dat'%(i,i,i))
        en_time = time.time()
        tmp_predict = en_time*1000 - st_time*1000
        print('***********************************************')
        print('prediction time is %s'%tmp_predict)
        print('***********************************************')
        writeFile('data/cross_data_py/%s/time-predict'%i,tmp_predict)