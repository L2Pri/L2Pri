#!/bin/bash

if [ x$1 != x ]; then
    n=$1
else
    n=40
fi

rq4="UA-all UO-all AO-all"

# learn
for rq4_key in $rq4
do
    for (( i=0; i<$n; i++ )) 
    do
        svm_rank/svm_rank_learn -c 1 data_rq4/$rq4_key/$i/train.dat data_rq4/$rq4_key/$i/svmrank-model.dat &
    done
    wait

    # predict
    for (( i=0; i<$n; i++ )) do
        svm_rank/svm_rank_classify data_rq4/$rq4_key/$i/test.dat data_rq4/$rq4_key/$i/svmrank-model.dat data_rq4/$rq4_key/$i/svmrank-pred.dat &
    done
    wait

    echo '$rq4_key is completed!'
done

wait




