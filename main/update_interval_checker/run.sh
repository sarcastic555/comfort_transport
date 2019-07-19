#!/bin/bash

###########
data_type="Bus"
bus_type="SeibuBus"
###

if [ -f out.txt ]; then
    rm out.txt
fi
if [ -f out_old.txt ]; then
    rm out_old.txt
fi

echo "data_type="${data_type}
echo "bus_type="${bus_type}

while :
do
    python checker.py ${data_type} ${bus_type} "out.txt"
    start_time=`date "+%s"`
    cp out.txt out_old.txt
    date
    dif=`diff out.txt out_old.txt | wc -l`
    counter=0
    while [ ${dif} -eq 0 ]; do
	sleep 1
	counter=`expr ${counter} + 1`
	python checker.py "Bus" "SeibuBus" "out.txt"
	dif=`diff out.txt out_old.txt | wc -l`
    done
    end_time=`date "+%s"`
    elapsed_time=`expr ${end_time} - ${start_time}`
    date
    echo "update interval is " ${elapsed_time} " sec"
done