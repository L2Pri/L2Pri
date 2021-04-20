#!/usr/bin/python
import xgboost as xgb
from sklearn.datasets import load_svmlight_file
import collections
import unittest
import sys
import pickle
#from sklearn.externals import joblib

root_path = '../data/cross_data_py/'

if len(sys.argv)!= 3:
    print('<Usage:> python rank_sklearning.py <subject_id> <subject_number>')
    sys.exit(0)
else:
    subject_id = int(sys.argv[1])
    subject_number = int(sys.argv[2])


#  This script demonstrate how to do ranking with XGBRanker
x_train, y_train, qid_train = load_svmlight_file(root_path + "/%s/train.dat"%subject_id,query_id=True)
#x_valid, y_valid = load_svmlight_file("mq2008.vali")
x_test, y_test, qid_test = load_svmlight_file(root_path + "/%s/test.dat"%subject_id,query_id=True)

qid_train_count = collections.Counter(qid_train)
qid_test_count = collections.Counter(qid_test)

group_train = []
for i in range(1,subject_number+1):
    if i in qid_train:
        group_train.append(qid_train_count[i])

#assertEqual(group_train,39)
#assertEqual(len(x_train),sum(group_train))


group_test = []
for i in range(1,subject_number+1):
    if i in qid_test:
        group_test.append(qid_test_count[i])

#assertEqual(len(x_test),sum(group_test))


params = {'objective': 'rank:pairwise',#'rank:ndcg', 
          'learning_rate': 0.1,
          'gamma': 1.0, 
          'min_child_weight': 0.1,
          'max_depth': 6,
          'n_estimators': 4}

model = xgb.sklearn.XGBRanker(**params)

model.fit(x_train, y_train, group_train, verbose=True,
          eval_set=[(x_test, y_test)], eval_group=[group_test])
pred = model.predict(x_test)
#print(pred)
#print(len(pred))
with open(root_path + '/%s/XGBRanker.pkl'%subject_id,'wb') as f:
    pickle.dump(model,f)
f = open(root_path + '/%s/XGBRanker_pred.dat'%subject_id,'w')
for item in pred:
    f.write('%s\n'%item)
f.close()
