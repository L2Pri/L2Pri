import os
import numpy as np

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

APFDcType = [
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
#'PerMutant',
#'Graph'
#'BestL2R'
'L2Rori'
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
    f = open('../result/rq1-new.csv','w')

    f.write('order,apfdc,app\n')
    for i,app in enumerate(apps):
        for subject in subjects:
            subject_path = path + subject + '/'
            if app == 'L2R':
                tmp_l2r = getAPFDc(subject_path + 'new-order/APFDcL2RStatement-use')
                f.write(str(i) + ',' + str(tmp_l2r) + ',' + app + '\n')
            elif app == 'L2Rori':
                tmp_l2r = getAPFDc(subject_path + 'new-order/APFDcOriFeatureBinaryStatement')
                f.write(str(i) + ',' + str(tmp_l2r) + ',' + app + '\n')
            else:
                try:
                    tmp_apfdc = getAPFDc(subject_path+'training/%s_200'%APFDcType[i])
                    f.write(str(i) + ',' + str(tmp_apfdc) + ',' + app + '\n')
                except:
                    print()
    f.close()



