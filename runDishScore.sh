for i in data/vectors/norm_64dim/norm_restaurant_*_vector64_type1.txt
do 
    ts -n -f sh -c "python DishScore.py $i" &
done
for i in data/vectors/norm_64dim/norm_restaurant_*_vector64_type2.txt
do 
    ts -n -f sh -c "python DishScore.py $i" &
done
for i in data/vectors/norm_64dim/norm_restaurant_*_vector64_type3.txt
do 
    ts -n -f sh -c "python DishScore.py $i" &
done
for i in data/vectors/norm_64dim/norm_restaurant_*_vector64_type4.txt
do 
    ts -n -f sh -c "python DishScore.py $i" &
done
