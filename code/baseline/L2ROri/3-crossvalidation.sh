#!/bin/bash

if [ x$1 != x ]; then
    n=$1
else
    n=40
fi

# learn
for (( i=20; i<$n; i++ )) do
    svm_rank/svm_rank_learn -c 1 data/cross_data_binary/$i/train.dat data/cross_data_binary/$i/svmrank-model.dat &
done
wait

# predict
for (( i=0; i<$n; i++ )) do
    svm_rank/svm_rank_classify data/cross_data_binary/$i/test.dat data/cross_data_binary/$i/svmrank-model.dat data/cross_data_binary/$i/svmrank-pred.dat &
done
wait

