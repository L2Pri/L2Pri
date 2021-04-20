import os,json,copy,random,sys
import numpy as np
import pickle
from tqdm import tqdm

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
    path = '../../subjects/experiment/'
    subjects = readFile(path + 'uselist-sc')
    #subjects.remove('jsoup')
    #apps = ['GT','GA','GE','ARP','TT','TA','TGE','TARP','TO']
    apps = ['cov','time']

    raw_data = open_pickle_file('./data/binary_data.pickle')
    #print(raw_data.keys())

    subject_qid_map = {}

    f = open('./data/l2r-format-data-binary.dat','w')
    #labels = getLabel('./data/ptp_label_single_task_apfdc_label.csv',subjects)
    q_id = 1
    for subject_id, subject in tqdm(enumerate(subjects)):
        subject_qid_map[subject_id] = []
        subject_path = path + subject + '/'
        subject_data = copy.deepcopy(raw_data[subject])
        #testList = list(subject_data['mutants'].keys())
        testList = readFile(subject_path + 'testList')
        mutants= readFile(subject_path + 'newmutantkill')
        mutants_num = len(mutants[0])
        
        for mutant_id in tqdm(range(mutants_num)):
            
            for test_id, test_name in enumerate(testList):
                tmp_line = []
                if mutants[test_id][mutant_id] == '1':
                    tmp_target = 1
                else:
                    tmp_target = 0
                tmp_line.append(str(tmp_target))
                tmp_qid = q_id
                tmp_line.append('qid:%s'%tmp_qid)
                for app_id,app in enumerate(apps):
                    tmp_line.append('%s:%s'%(app_id+1,subject_data['scores'][test_name][app]))
                f.write(' '.join(tmp_line) + ' # %s\n'%test_name)

                del tmp_line
            subject_qid_map[subject_id].append(q_id)
            q_id += 1
    f.close()
    save_pickle_file(subject_qid_map, './data/subject_qid_map.pickle')
        