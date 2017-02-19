#!/bin/zsh

#for i in data/cooccurrence/restaurant_*_cooccur_type1.txt
#do
#    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
#    filename=$(echo $i | cut -d'/' -f 3)
#    num=$(echo $filename | egrep -o "_([0-9]+)_" | egrep -o "[0-9]+" )
#    echo $num
#    ts -n -f sh -c "./line -train $i -output data/vectors/64dim/restaurant_"$num"_vector64_type1.txt -size 64 -order 1 -negative 5 -samples 20 -threads 1
#    ./normalize -input data/vectors/64dim/restaurant_"$num"_vector64_type1.txt -output data/vectors/norm_64dim/norm_restaurant_"$num"_vector64_type1.txt -binary 0
#    #" &
#    echo "-------------------------------------------"
#done    
#ts -S 20

#for i in data/cooccurrence/restaurant_*_cooccur_type2.txt
#do
#    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
#    filename=$(echo $i | cut -d'/' -f 3)
#    num=$(echo $filename | egrep -o "_([0-9]+)_" | egrep -o "[0-9]+" )
#    echo $num
#    ts -n -f sh -c "./line -train $i -output data/vectors/64dim/restaurant_"$num"_vector64_type2.txt -size 64 -order 1 -negative 5 -samples 20 -threads 1
#    ./normalize -input data/vectors/64dim/restaurant_"$num"_vector64_type2.txt -output data/vectors/norm_64dim/norm_restaurant_"$num"_vector64_type2.txt -binary 0
#    " &
#    echo "-------------------------------------------"
#done
#ts -S 20

for i in data/cooccurrence/restaurant_*_cooccur_type3.txt
do
    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
    filename=$(echo $i | cut -d'/' -f 3)
    num=$(echo $filename | egrep -o "_([0-9]+)_" | egrep -o "[0-9]+" )
    echo $num
    ts -n -f sh -c "./line -train $i -output data/vectors/64dim/restaurant_"$num"_vector64_type3.txt -size 64 -order 1 -negative 5 -samples 20 -threads 1
    ./normalize -input data/vectors/64dim/restaurant_"$num"_vector64_type3.txt -output data/vectors/norm_64dim/norm_restaurant_"$num"_vector64_type3.txt -binary 0
    " & 
    echo "-------------------------------------------"
done 
ts -S 20

#for i in data/cooccurrence/restaurant_*_cooccur_type4.txt
#do
#    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
#    filename=$(echo $i | cut -d'/' -f 3)
#    num=$(echo $filename | egrep -o "_([0-9]+)_" | egrep -o "[0-9]+" )
#    echo $num
#    ts -n -f sh -c "./line -train $i -output data/vectors/64dim/restaurant_"$num"_vector64_type4.txt -size 64 -order 1 -negative 5 -samples 20 -threads 1
#    ./normalize -input data/vectors/64dim/restaurant_"$num"_vector64_type4.txt -output data/vectors/norm_64dim/norm_restaurant_"$num"_vector64_type4.txt -binary 0
#    " & 
#    echo "-------------------------------------------"
#done 
#ts -S 20
