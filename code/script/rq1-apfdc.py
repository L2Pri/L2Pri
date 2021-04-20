import os
import numpy as np

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

APFDType = [
'APFDcL2RStatement-use',
'APFDcGTStatement',
'APFDcGAStatement',
'APFDcGEStatement',
'APFDcARPStatement',
'APFDcTTStatement',
'APFDcTAStatement',
'APFDcTGEStatement',
'APFDcTARPStatement',
'APFDcTOStatement',
'APFDcOriFeatureBinaryStatement'
]

apps = [
'L2R',
'UGT',
'UGA',
'UGE',
'UARP',
'AGT',
'AGA',
'AGE',
'AARP',
'TO',
'L2Rori'
#'PerMutant',
#'Graph'
#'BestL2R'
]


def getAPFDc(filepath):
    tmp = readFile(filepath)
    for i in range(len(tmp)):
        tmp[i] = eval(tmp[i])
    #print(np.mean(t1))
    return np.mean(tmp)


def test():
    path = '/devdata2/zjy/fse-extension/subjects/experiment/java-uuid-generator/'
    #print(t2)
    for app in APFDType:
        t2 = getAPFDc(path + 'training/%s_200'%app)
        print('%s : %s'%(app,t2))
    print('*************')
    t1 = getAPFDc(path+'new-order/APFDcGraphStatement')
    #t2 = getAPFDc(path+'training/APFDcARPStatement_200')
    print('%s : %s'%('APFDcGraphStatement',t1))
    print('*************')
    t3 = getAPFDc(path+'new-order/APFDcL2RStatement')
    print('%s : %s'%('APFDcL2RStatement',t3))

#test()


if __name__ == '__main__':
    path = '/devdata2/zjy/fse-extension/subjects/experiment/'
    subjects = readFile(path + 'uselist-sc')
    #subjects.remove('jsoup')
    f = open('../result/rq1-apfdc-new','w')
    info_dict = {}
    sorted_list = []
    for i,subject in enumerate(subjects):
        subject_path = path + subject + '/'
        tmp_list = []
        for j,app in enumerate(APFDType):
            if j==0:
                l2r = getAPFDc(subject_path + 'new-order/APFDcL2RStatement-use')
                tmp_str = str(round(l2r,3))
                tmp_list.append(r'\textbf{'+tmp_str+'0'*(5-len(tmp_str))+'}')
            elif j == 10:
                l2rori = getAPFDc(subject_path + 'new-order/APFDcOriFeatureBinaryStatement')
                tmp_str = str(round(l2rori,3))
                tmp_list.append(tmp_str+'0'*(5-len(tmp_str)))
            else:
                tmp_apfdc = getAPFDc(subject_path+'training/%s_200'%app)
                tmp_str = str(round(tmp_apfdc,3))
                tmp_list.append(tmp_str+'0'*(5-len(tmp_str)))
        #print(tmp_list)
        #print(type(tmp_list))
        #print('& '.join(tmp_list))
        info_dict[subject.lower()] = '& '.join(tmp_list)
        sorted_list.append(subject.lower())
    sorted_list.sort()
    tt = ['rome','dictomaton']
    for i,subject in enumerate(sorted_list):
        f.write('%s& '%(i+1) + info_dict[subject] + r' \\' + '\n')
        if subject in tt:
            print('%s : %s'%(i+1, subject))

    f.close()



