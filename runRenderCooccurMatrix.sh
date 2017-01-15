for i in ../data/line-data/vectors/200dim/restaurant_1_vector200.txt
do
    ts -n -f sh -c "python RenderCooccurMatrix.py $i" &
done
ts -S 15
