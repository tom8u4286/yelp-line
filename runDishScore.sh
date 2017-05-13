#!/bin/zsh
num=$(ls -l data/vectors/norm_64dim/ | egrep -c 'restaurant')
for ((i=1;i<=$num;i++));
do 
    ts -n -f sh -c "python DishScore.py $i" &
done
ts -S 20
