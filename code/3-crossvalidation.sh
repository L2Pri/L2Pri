#!/bin/bash

if [ x$1 != x ]; then
    n=$1
else
    n=40
fi

# learn
for (( i=0; i<$n; i++ )) do
    svm_rank/svm_rank_learn -c 1 data/cross_data_best/$i/train.dat data/cross_data_best/$i/svmrank-model.dat &
done
wait

# predict
for (( i=0; i<$n; i++ )) do
    svm_rank/svm_rank_classify data/cross_data_best/$i/test.dat data/cross_data_best/$i/svmrank-model.dat data/cross_data_best/$i/svmrank-pred.dat &
done
wait

