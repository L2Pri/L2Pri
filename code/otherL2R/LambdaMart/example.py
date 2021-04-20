from lambdamart import LambdaMART 
import numpy as np
import copy
from tqdm import tqdm
import sys

root_path = '../data/cross_data_py/'

if len(sys.argv)!= 2:
    print('<Usage:> python rank_sklearning.py <subject_id>')
    sys.exit(0)
else:
    subject_id = int(sys.argv[1])
    #subject_number = int(sys.argv[2])

def get_data(file_loc):
    f = open(file_loc, 'r')
    data = []
    for line in f:
        new_arr = []
        arr = line.split(' #')[0].split()
        ''' Get the score and query id '''
        score = arr[0]
        q_id = arr[1].split(':')[1]
        new_arr.append(int(score))
        new_arr.append(int(q_id))
        arr = arr[2:]
        ''' Extract each feature from the feature vector '''
        for el in arr:
            new_arr.append(float(el.split(':')[1]))
        data.append(copy.deepcopy(new_arr))
    f.close()
    #print('length : %s'%len(data))
    return np.array(data)

def main():
    training_data = get_data(root_path + '/%s/train.dat'%subject_id)
    test_data = get_data(root_path + '/%s/test.dat'%subject_id)
    model = LambdaMART(
    training_data=training_data, 
    number_of_trees=100, 
    learning_rate=0.01)
    
    model.fit()

    #average_ndcg, predicted_scores = model.validate(test_data)
    predicted_scores = model.predict(test_data[:,1:])
    #print(predicted_scores)

    #model.save('example_model')
    model.save(root_path + '/%s/lambdaMART'%subject_id)
    f = open(root_path + '/%s/lambdaMART.dat'%subject_id,'w')
    for item in predicted_scores:
        f.write('%s\n'%item)
    f.close()

    #model = LambdaMART()
    #model.load('example_model.lmart')
    #print(len(test_data[1]))
    #print(len(test_data[:,1:]))
    #print(np.shape(test_data))
    #print(test_data)

if __name__ == '__main__':
    main()