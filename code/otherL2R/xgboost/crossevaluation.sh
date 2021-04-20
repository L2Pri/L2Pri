#!/bin/bash

n=40

for (( i=0; i<$n; i++ )) do
    #svm_rank/svm_rank_learn -c 1 data/cross_data_best/$i/train.dat data/cross_data_best/$i/svmrank-model.dat &
    python rank_sklearning.py $i 40
done
wait