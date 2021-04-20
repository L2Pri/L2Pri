import os,json,copy,random,sys
import numpy as np
import pickle
from tqdm import tqdm
import copy

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

def tt(filepath):
    with open(filepath, 'rb') as input_file:
        try:
            return pickle.load(input_file)
        except EOFError:
            return None

def save_pickle_file(data, file_path):
    '''
    Save the file of data
    :param data: The data of input
    :param file_path: The path of file
    :return:
    '''
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def getLabel(filepath,subjects):
    label_dict = {}
    tmp_list = readFile(filepath)
    for line in tmp_list[1:]:
        tmp = line.split(',')
        label_dict[tmp[0]] = tmp[-1]
    return label_dict


if __name__ == '__main__':
    path = '../subjects/experiment/'
    subjects = readFile(path + 'uselist-sc')
    #subjects.remove('jsoup')

    rq4 = {'UA-all':['GT','GA','GE','ARP','TT','TA','TGE','TARP'],
            'UO-all':['GT','GA','GE','ARP','TO'],
            'AO-all':['TT','TA','TGE','TARP','TO']}

    raw_data = open_pickle_file('./data/raw_data.pickle')
    #print(raw_data.keys())

    for rq4_key in tqdm(rq4.keys()):
        apps = copy.deepcopy(rq4[rq4_key])
        f = open('./data_rq4/l2r-format-data-%s.dat'%rq4_key,'w')
        #f_best = open('./data/l2r-format-data-app.dat','w')
        #labels = getLabel('./data/ptp_label_single_task_apfdc_label.csv',subjects)
        for subject_id, subject in tqdm(enumerate(subjects)):
            subject_path = path + subject + '/'
            subject_data = copy.deepcopy(raw_data[subject])
            testList = list(subject_data['mutants'].keys())
            #bestList = readFile(subject_path + '/training/%sStatement_200'%labels[subject])
            #test_num = len(testList)
            testPre = []
            #print(subject_data.keys())
            #print(subject_data['mutants'])
            for test_item in testList:
                #print(subject_data['mutants'])
                #print(subject)
                #print('%s , %s'%(subject_data['mutants'][test_item],subject_data['time'][test_item])) 
                testPre.append(subject_data['mutants'][test_item]/subject_data['time'][test_item])
            rank_list = copy.deepcopy(testPre)
            rank_list = list(set(rank_list))
            #rank_list.sort(reverse=True)
            rank_list.sort()
            for test_id, test_name in enumerate(testList):
                tmp_line = []
                tmp_target = rank_list.index(testPre[test_id]) + 1
                tmp_line.append(str(tmp_target))
                tmp_qid = subject_id + 1
                tmp_line.append('qid:%s'%tmp_qid)
                for app_id,app in enumerate(apps):
                    tmp_line.append('%s:%s'%(app_id+1,subject_data['scores'][test_name][app]))
                f.write(' '.join(tmp_line) + ' # %s\n'%test_name)

                #tmp_target_best = test_num - bestList.index(test_name)
                #tmp_line[0] = str(tmp_target_best)
                #f_best.write(' '.join(tmp_line) + ' # %s\n'%test_name)
                del tmp_line
        f.close()
        #assert(0)
        