import os,copy,sys,random
from tqdm import tqdm
import numpy as np
import pickle

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def open_pickle_file(file_path):
    '''
    Open the file of bin
    :param file_path: path of file
    :return:
    '''
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
        #print(data[0].head)
        #print(data[0].body)
        #print(data[0].foot)
    return data


def save_pickle_file(data, file_path):
    '''
    Save the file of data
    :param data: The data of input
    :param file_path: The path of file
    :return:
    '''
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def getIndex(t_ori,t_sorted):
    tmp_index = []
    for test_name in t_ori:
        tmp_index.append(t_sorted.index(test_name))
    return tmp_index

def Index2Score(t1):
    tmp_score = []
    tmp_len = len(t1)
    for i in t1:
        tmp_score.append((tmp_len-i)/tmp_len)
    return tmp_score

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

if __name__ =='__main__':
    path = '../../subjects/experiment/'
    subjects = readFile(path + 'uselist-sc')
    apps = ['GT','GA','GE','ARP','TT','TA','TGE','TARP','TO']

    raw_data = {}

    for subject in tqdm(subjects):
        subject_data = {'mutants':{},'scores':{},'time':{}}
        subject_path = path + subject + '/'
        testList = readFile(subject_path + 'testList')
        if os.path.exists(subject_path + 'exeTime') == True:
            timeList = readFile(subject_path + 'exeTime')
        elif os.path.exists(subject_path + 'exeTime.txt') == True:
            timeList = readFile(subject_path + 'exeTime.txt')
        else:
            print('Err: testing time file not exists!')
            assert(0)
        mutantList = readFile(subject_path + 'newmutantkill')

        covList = readFile(subject_path + 'stateMatrix.txt')

        cov_score = []
        time_score = []
        per_score = []
        for i,key in enumerate(testList):
            cov_score.append(covList[i].count('1'))
            time_score.append(eval(timeList[i]))
            per_score.append(covList[i].count('1')/eval(timeList[i]))
        cov_score = normalization(cov_score)
        time_score = normalization(time_score)
        per_score = normalization(per_score)

        for i in range(len(testList)):
            test_name = testList[i]
            subject_data['scores'][test_name] = {'cov':cov_score[i],
                                       'time':time_score[i],
                                       'per':per_score[i]}
            #subject_data['mutants'][test_name] = mutantList[i].count('1')
            tmp = []
            for j in range(len(mutantList[i])):
                if mutantList[i][j] == '1':
                    tmp.append(j)
            subject_data['mutants'][test_name] = copy.deepcopy(tmp)
            del tmp
            subject_data['time'][test_name] = eval(timeList[i])
            raw_data[subject] = copy.deepcopy(subject_data)
            #count += 1
        #print(raw_data)
        #print(count)
        #input('check...')
    save_pickle_file(raw_data,'./data/binary_data.pickle')




