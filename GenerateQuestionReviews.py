import json
import random
import numpy as np
import sys
from operator import itemgetter

#Dish Extraction
f_dict = open('data/restaurant_dict_list/restaurant_dict_1.json')
rest_dict = json.load(f_dict)
menu = [dish for dish in rest_dict['menu'] if dish['count'] >= 10]

menu_length = len(menu)
num1, num2 = int(menu_length*0.27), int(menu_length*0.74)

dish_list = []
for num in random.sample(range(0, num1), 3):
    dish_list.append(menu[num])

for num in random.sample(range(num1, num2), 4):
    dish_list.append(menu[num])

for num in random.sample(range(num2, menu_length), 3):
    dish_list.append(menu[num])

#top3 = [menu[num] for num in random.sample(range(0, num1+1), 3)]
#mid3 =  [menu[num] for num in random.sample(range(num1, num2+1), 4)]
#bot3 =  [menu[num] for num in random.sample(range(num2, menu_length+1), 3)]
for dish in dish_list:
    print dish

f_review = open('data/compare/restaurant_1.json')
review_dic = json.load(f_review)
new_review_dic_list = []
for review in review_dic:
    length = len(review['new'].split(' '))
    review['len'] = length
    new_review_dic_list.append(review)

sorted_review_list = sorted(new_review_dic_list, key=itemgetter('len'))
raw_reviews = [review['old'].replace('\n','') for review in sorted_review_list]
backend_reviews = [review['new'] for review in sorted_review_list]


for dish in dish_list:
    dish_ar = dish['name_ar']
    dish_reviews = []

    for review in sorted_review_list:
        if dish_ar in review['new']:
            dish_reviews.append(review)
    select_list = []
    if len(dish_reviews) > 10:
        percent02 = int(len(dish_reviews)*0.2)
        percent04 = int(len(dish_reviews)*0.4)
        percent06 = int(len(dish_reviews)*0.6)
        percent08 = int(len(dish_reviews)*0.8)

        for num in random.sample(range( 0, percent02), 2):
            select_list.append(num)
        for num in random.sample(range( percent02, percent04), 2):
            select_list.append(num)
        for num in random.sample(range( percent04, percent06), 2):
            select_list.append(num)
        for num in random.sample(range( percent06, percent08), 2):
            select_list.append(num)
        for num in random.sample(range( percent08, len(dish_reviews)), 2):
            select_list.append(num)
    else:
        select_list = range(0, len(dish_reviews))

    extract_reviews = []
    for num in select_list:
        extract_reviews.append(dish_reviews[num]['old'])
    f_out = open('../TestingReviews/%s.txt'%dish_ar,'w+')
    f_out.write('\n'.join(extract_reviews))


