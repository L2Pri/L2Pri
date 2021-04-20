import os
from tqdm import tqdm

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

if __name__ == '__main__':
    path = '/devdata2/zjy/fse-extension/subjects/experiment/'
    path_source = '/devdata2/zjy/fse-extension/subjects/source/'
    subjects = readFile(path + 'uselist-sc')

    info_dict = {}

    sorted_list = []

    for subject in tqdm(subjects):
        subject_path = path + subject + '/'
        subject_path_source = path_source + subject + '/'
        testlist = readFile(subject_path + 'testList')
        tmp_main = subject_path_source + 'src/main/'
        tmp_test = subject_path_source + 'src/test/'

        os.chdir(subject_path_source)
        os.system('mvn test > mvn_log')
    