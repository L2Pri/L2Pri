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
    path = './subjects/experiment/'
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

        gt = readFile(subject_path + 'training/GTStatement')
        ga = readFile(subject_path + 'training/GAStatement')
        ge = readFile(subject_path + 'training/GEStatement')
        arp = readFile(subject_path + 'training/ARPStatement')
        tt = readFile(subject_path + 'training/TTStatement')
        ta = readFile(subject_path + 'training/TAStatement')
        tge = readFile(subject_path + 'training/TGEStatement')
        tarp = readFile(subject_path + 'training/TARPStatement')
        to = readFile(subject_path + 'training/TOStatement')

        gt_index = getIndex(testList,gt)
        ga_index = getIndex(testList,ga)
        ge_index = getIndex(testList,ge)
        arp_index = getIndex(testList,arp)
        tt_index = getIndex(testList,tt)
        ta_index = getIndex(testList,ta)
        tge_index = getIndex(testList,tge)
        tarp_index = getIndex(testList,tarp)
        to_index = getIndex(testList,to)

        gt_score = Index2Score(gt_index)
        ga_score = Index2Score(ga_index)
        ge_score = Index2Score(ge_index)
        arp_score = Index2Score(arp_index)
        tt_score = Index2Score(tt_index)
        ta_score = Index2Score(ta_index)
        tge_score = Index2Score(tge_index)
        tarp_score = Index2Score(tarp_index)
        to_score = Index2Score(to_index)

        #print(subject)
        #print(len(testList))
        #print(len(set(testList)))
        #count = 0
        for i in range(len(testList)):
            test_name = testList[i]
            subject_data['scores'][test_name] = {'GT':gt_score[i],
                                       'GA':ga_score[i],
                                       'GE':ge_score[i],
                                       'ARP':arp_score[i],
                                       'TT':tt_score[i],
                                       'TA':ta_score[i],
                                       'TGE':tge_score[i],
                                       'TARP':tarp_score[i],
                                       'TO':to_score[i]}
            subject_data['mutants'][test_name] = mutantList[i].count('1')
            subject_data['time'][test_name] = eval(timeList[i])
            raw_data[subject] = copy.deepcopy(subject_data)
            #count += 1
        #print(raw_data)
        #print(count)
        #input('check...')
    save_pickle_file(raw_data,'./data/raw_data.pickle')

