#!/bin/zsh
for ((i=1;i<=264;i++));
do   
    ts -n -f sh -c "python new_ReviewParser.py $i" &
done
ts -S 20

