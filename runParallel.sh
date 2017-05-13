#!/bin/zsh
num=$(ls -l data/reviews/ | egrep -c 'restaurant')
for ((i=1;i<=$num;i++));
do   
    ts -n -f sh -c "python new_ReviewParser.py $i" &
done
ts -S 20

