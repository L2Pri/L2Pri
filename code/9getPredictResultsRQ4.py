import os
import copy
from tqdm import tqdm

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def getTestList(filepath):
    tmp_testlist = []
    tmp = readFile(filepath)
    qid = eval(tmp[0].split(' ')[1].split(':')[-1])
    for line in tmp:
        test_name = line.split(' # ')[1]
        tmp_testlist.append(test_name)
    return (tmp_testlist,qid)

# basic quick sort
def quickSort(temp_list):
        less = []
        pivotList = []
        more = []
        if len(temp_list) <= 1:
                return temp_list
        else:
                pivot = temp_list[0]
                for i in temp_list:
                        if i[1] < pivot[1]:
                                less.append(i)
                        elif i[1] > pivot[1]:
                                more.append(i)
                        else:
                                pivotList.append(i)
        less = quickSort(less)
        more = quickSort(more)
        return more + pivotList + less

# sort with the test name and test coverage information
def quick_sort(temp_name, temp_score):
    temp_list = []
    for i in range(len(temp_score)):
        temp_list.append((temp_name[i],eval(temp_score[i])))
    return quickSort(temp_list)


if __name__ == '__main__':
    path = '../subjects/experiment/'
    subjects = readFile(path + 'uselist-sc')

    rq4 = {'UA-all':['GT','GA','GE','ARP','TT','TA','TGE','TARP'],
            'UO-all':['GT','GA','GE','ARP','TO'],
            'AO-all':['TT','TA','TGE','TARP','TO']}

    for rq4_key in rq4.keys():
        #if rq4_key not in ['1-UGT','1-AGT','1-TO']:
        #    continue
        tt = os.listdir('./data_rq4/%s/'%rq4_key)
        #tt = [6]

        for i in tqdm(tt):
            pre_path = './data_rq4/%s/%s/'%(rq4_key,i)
            pre_result = readFile(pre_path + 'svmrank-pred.dat')
            testlist,qid = getTestList(pre_path + 'test.dat')
            sorted_list = quick_sort(testlist,pre_result)
            #print(sorted_list)
            #print(qid)
            subject = subjects[qid-1]
            subject_path = path + subject + '/'
            if os.path.exists(subject_path + 'new-order/') == False:
                os.makedirs(subject_path + 'new-order/')
            f = open(subject_path + 'new-order/L2RStatement-%s'%rq4_key,'w')
            for item in sorted_list:
                f.write('%s\n'%item[0])
            f.close()


