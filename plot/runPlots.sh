#!/bin/zsh
#for i in ../data/backend_reviews/restaurant_1_first100.txt
for ((i=1; i <=10; i++)) ;
do
    python PlotDishScoreAndFrqxZScore.py $i 3
done

for ((i=1; i <=10; i++)) ;
do
    python PlotDishScoreAndNormFrq.py $i 3
done

for ((i=1; i <=10; i++)) ;
do
    python PlotDishScoreAndSentiCosVar.py $i 3
done

for ((i=1; i <=10; i++)) ;
do
    python PlotDishScoreAndZScore.py $i 3
done
