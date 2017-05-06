#for i in data/vectors/64dim/restaurant_*_vector64_type1.txt
#do
#    ts -n -f sh -c "python Tsne.py $i" &
#done
#ts -S 20
#for i in data/vectors/64dim/restaurant_*_vector64_type2.txt
#do
#    ts -n -f sh -c "python Tsne.py $i" &
#done
#ts -S 20
for i in data/vectors/64dim/restaurant_*_vector64_type3.txt
do
    ts -n -f sh -c "python Tsne.py $i" &
done
ts -S 20
#for i in data/vectors/64dim/restaurant_*_vector64_type4.txt
#do
#    ts -n -f sh -c "python Tsne.py $i" &
#done
#ts -S 20
