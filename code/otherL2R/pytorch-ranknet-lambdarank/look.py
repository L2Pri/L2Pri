import os

def readFile(filepath):
    with open(filepath) as f:
        content = f.read()
    return content.splitlines()

if __name__ == '__main__':
    path = '/devdata3/zjy/L2RTCP/code/data/cross_data_py/'

    empty_list = []
    not_equal_list = []
    for i in range(40):
        subject_path = path + str(i) + '/'
        if os.path.exists(subject_path+'RankNet_pred.dat') == False:
            empty_list.append(i)
        else:
            tmp = readFile(subject_path+'RankNet_pred.dat')
            tmp2 = readFile(subject_path+'svmrank-pred.dat')
            if len(tmp) == 0:
                empty_list.append(i)
            if len(tmp) != len(tmp2):
                not_equal_list.append(i)
    print('empty list is (%s)  : %s'%(len(empty_list),str(empty_list)))
    print('not equal list : %s'%str(not_equal_list))
