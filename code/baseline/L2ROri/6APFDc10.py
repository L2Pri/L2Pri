import copy
import os
import re
import shutil
import  xml.dom.minidom
from bs4 import BeautifulSoup
import random
from tqdm import tqdm
import numpy as np
from tqdm import tqdm

#file have the handled subject list
#SubjectListFile = 'anonymous/projects/hbase-1.2.2/SuccessFile.txt'# anonymous processing
SubjectRootPath = '../../subjects/experiment/' # anonymous processing


sequenceType = ['OriFeatureBinaryStatement']
APFDType = ['APFDcOriFeatureBinaryStatement']

#mutantSum = 0
testSum = 0
groupSum = 0
timeSum = 0

def readFile(filepath):
    with open(filepath) as f:
        content = f.read()
    return content.splitlines()

def readKillMatrix(readMutantPath):
    '''
    readfile = open(readTestPath)
    lines = readfile.readlines()
    testSum = len(lines)
    readfile.close()
    '''
    #global mutantSum
    #global groupSum
    readfile = open(readMutantPath)
    lines = readfile.readlines()
    #mutantSum = len(lines)
    readfile.close()
    #groupSum = mutantSum / 5
    #killMatrix = [[0 for col in range(testSum)] for row in range(mutantSum)]
    killMatrix = []
    for line in lines:
        kills = list(line.strip())
        killMatrix.append(kills)
    return killMatrix

def readSubjectList(readFilePath):
    SubjectList = []
    readFile = open(readFilePath)
    for line in readFile:
        SubjectList.append(line.strip())
        readFile.close()
    return SubjectList

def readTestList(readpath):
    global testSum
    testMap = {}
    count = 0
    readfile = open(readpath)
    for line in readfile:
        line = line.strip()
        testMap[line] = count
        count = count + 1
    readfile.close()
    testSum = count
    return testMap
	
def readTimeList(readpath):
    global timeSum
    timeSum = 0
    timeList = []
    readfile = open(readpath)
    for line in readfile:
        line = float(line.strip())
        timeSum = timeSum + line
        timeList.append(line)
    readfile.close()
    return timeList


def calculateAPFDc(readpath, writepath, mutantGroup, killMatrix, TestMap, timeList, tcpTech):
    global groupSum
    sequence = []
    tmp_avg = []
    #print groupSum
    #print(readpath)
    #translate the sequence 
    readfile = open(readpath)
    for line in readfile:
        line = line.strip()
        sequence.append(TestMap[line])
        #sequence.append(line)
    readfile.close()

    writefile = open(writepath, 'w')
    #print(mutantGroup)
    for i in range(0, groupSum):
        mutantlist = mutantGroup[i]
        APFDcvalue = singleAPFDc(sequence, mutantlist, killMatrix, timeList)
        #print(APFDcvalue)
        #assert(0)
        tmp_avg.append(APFDcvalue)
        #print('apfdc is : %s'%APFDvalue)
        #print APFDvalue
        #input('check...')
        writefile.write(str(APFDcvalue) + '\n')
    #print(writepath)
    #raw_input('check...')
    writefile.close()
    #print('%s : %s'%(tcpTech,np.mean(tmp_avg)))

def singleAPFDc(sequence, mutantlist, killMatrix, timeList):
    APFDcvalue = 0
    tmpMutantList = []
    for i in range(len(mutantlist)):
        currentMutant = mutantlist[i]
        tmpcount = 0
        for j in range(0, len(sequence)):
            #print('%s - %s, %s'%(j,testSum,len(sequence)))
            currentTest = sequence[j]
            #if killMatrix[currentMutant][currentTest] == '1':
            if killMatrix[currentTest][currentMutant] == '1':
                #print('single : %s is killed by %s, currentTest time is %s'%(currentMutant,currentTest,timeList[currentTest]))
                for k in range(j, len(sequence)):
                    tmpTest = sequence[k]
                    tmpcount = tmpcount + timeList[tmpTest]
                tmpcount = tmpcount - 0.5 * timeList[currentTest]
                break
        APFDcvalue = APFDcvalue + tmpcount
        #print(tmpcount)
    APFDcvalue = APFDcvalue*1.0/ (sum(timeList) * len(mutantlist))
    #print(mutantlist)
    return APFDcvalue

def readMutantGroup(readpath):
    global groupSum
    readfile = open(readpath)
    lines = readfile.readlines()
    readfile.close()
    groupSum = len(lines)
    mutantGroup = []
    for line in lines:
        line = line.strip()
        items = line.split(' ')
        tmp = []
        for item in items:
            tmp.append(int(item))
        mutantGroup.append(copy.deepcopy(tmp))
    #print(mutantGroup)
    #raw_input('check...')
    return mutantGroup

def readSubjectList(readFilePath):
    SubjectList = []
    readFile = open(readFilePath)
    for line in readFile:
        SubjectList.append(line.strip())
    readFile.close()
    return SubjectList

if __name__ == '__main__':
    SubjectList = readSubjectList(SubjectRootPath + '/uselist-sc')
    #SubjectList.remove('jsoup')
    #SubjectList = ['commons-email']
    for sub in tqdm(SubjectList):
        print 'SUBJECT ' + sub
        subpath = SubjectRootPath + sub + '/'
        timeList_ori = readTimeList(subpath + '/exeTime')
        for train_index in range(1):
            TestMap = readTestList(subpath + '/testList')
            # mutant group
            mutantGroup = readMutantGroup(subpath + '/mutantGroup-all')
            # all mutants
            timeList = readTimeList(subpath + '/exeTime')
            killMatrix = readKillMatrix(subpath + 'newmutantkill')
            for i in range(0, len(sequenceType)):
                readdir = subpath + '/new-order/'
                #os.system('cp %s %s'%(subpath+'/training/Optimal_200',subpath+'/new-order/Optimal'))
                calculateAPFDc(readdir + sequenceType[i] ,  readdir + APFDType[i] ,  mutantGroup,  killMatrix, TestMap, timeList,sequenceType[i])
            del timeList
            del killMatrix
            del mutantGroup
            #print('%s - %s is completed!'%(sub,train_index))
            #input('check...')
