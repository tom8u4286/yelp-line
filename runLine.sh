
for i in data/cooccurrence/restaurant_1_cooccur.txt
do
    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
    filename=$(echo $i | cut -d'/' -f 3)
    num=$(echo $filename | egrep -o "[0-9]+")
    echo $num
    #echo $filename
    ts -n -f sh -c "./line -train $i -output data/vectors/64dim/restaurant_"$num"_vector64.txt -size 64 -order 1 -negative 5 -samples 20 -threads 1
    ./normalize -input data/vectors/64dim/restaurant_"$num"_vector64.txt -output data/vectors/norm_64dim/norm_restaurant_"$num"_vector64.txt -binary 0
    #" 
    echo "-------------------------------------------"
done    
#ts -S 20
