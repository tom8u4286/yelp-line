
#for i in ../data/backend_reviews/restaurant_1_first100.txt
for i in ../data/backend_reviews/restaurant_1.txt
do
    ts -n -f sh -c "python glove.py $i" &
done
ts -S 17
