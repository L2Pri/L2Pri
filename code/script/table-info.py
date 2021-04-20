import os

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


def parsetime(filepath):
    tmp = readFile(filepath)

    if 'BUILD SUCCESS' in tmp[-5]:
        #print(tmp[-3].split(' '))
        tmp_list = tmp[-3].split(' ')
        if tmp_list[-1] == 's':
            tmp_time = eval(tmp_list[3])
        elif tmp_list[-1] == 'min':
            cal_time = tmp_list[3].split(':')
            for i in range(len(cal_time)):
                while True:
                    if cal_time[i][0] == '0':
                        cal_time[i] = cal_time[i][1:]
                        continue
                    else:
                        break
            tmp_time = eval(cal_time[0])*60 + eval(cal_time[1])
        else:
            print(tmp_list)
            assert(0)
        #print(tmp_time)
        #assert(0)
        return tmp_time
    else:
        return False


if __name__ == '__main__':
    path = '/devdata2/zjy/fse-extension/subjects/experiment/'
    path_source = '/devdata2/zjy/fse-extension/subjects/source/'
    subjects = readFile(path + 'uselist-sc')

    info_dict = {}

    sorted_list = []
    err_list = []

    for i,subject in enumerate(subjects):
        subject_path = path + subject + '/'
        subject_path_source = path_source + subject + '/'
        testlist = readFile(subject_path + 'testList')
        tmp_main = subject_path_source + 'src/main/'
        tmp_test = subject_path_source + 'src/test/'

        tmp1 = execCmd('sloc ' + tmp_main).splitlines()
        #print(tmp1)
        for tmp_line in tmp1:
            #print(tmp_line)
            if 'Source' in tmp_line:
                #print(tmp_line)
                tmp_info_source = int(tmp_line.split(' :  ')[1])
                #print(tmp_info_source)
                #assert(0)
        tmp2 = execCmd('sloc ' + tmp_test).splitlines()
        #print(tmp2)
        for tmp_line in tmp2:
            #print(tmp_line)
            if 'Source' in tmp_line:
                #print(tmp_line)
                tmp_info_test = int(tmp_line.split(' :  ')[1])
                #print(tmp_info_source)
                #assert(0)
        #print('%s, %s'%(tmp_info_source,tmp_info_test))
        mutants = readFile(subject_path + 'usemutant-info')

        time = parsetime(subject_path_source + 'mvn_log')
        if time == False:
            err_list.append(subject)

        info_dict[subject.lower()] = [str(tmp_info_source),str(tmp_info_test),str(len(testlist)),str(time),str(len(mutants))]
        sorted_list.append(subject.lower())
        print(str(i) + ' ' + subject.lower() + ' ' + str(info_dict[subject.lower()]))

        #assert(0)
    sorted_list.sort()
    sloc_list = []
    tloc_list = []
    test_list = []
    time_list = []
    mutant_list = []
    f = open('table-info.tex','w')
    for i,subject in enumerate(sorted_list):
        f.write(str(i+1) + '&' + subject.split('/')[-1] + '& ')
        f.write('& '.join(info_dict[subject]))
        f.write(r' \\')
        f.write('\n')
        sloc_list.append(eval(info_dict[subject][0]))
        tloc_list.append(eval(info_dict[subject][1]))
        test_list.append(eval(info_dict[subject][2]))
        time_list.append(eval(info_dict[subject][3]))
        mutant_list.append(eval(info_dict[subject][4]))
    f.close()

    print(sum(sloc_list))
    print(sum(tloc_list))
    print(sum(test_list))
    print(sum(time_list))
    print(sum(mutant_list))


