#!/bin/bash
if [ x$1 != x ]; then
    n=$1
else
    n=40
fi

rq4="UA-all UO-all AO-all"

# split
for (( i=0; i<$n; i++ )) 
do
    for rq4_key in $rq4
    do
        echo $rq4_key
        python2 7splitRQ4.py $i $n $rq4_key &
        #echo $rq4_key
    done
done
wait
echo "$n-fold split finished."
