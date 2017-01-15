for i in ../data/line-data/vectors/200dim/restaurant_*_cooccur.txt
do
    ts -n -f sh -c "python Tsne.py $i" &
done
ts -S 5
