import json
import random
import numpy as np
import sys
import re
import unicodedata
from operator import itemgetter

rest_num = sys.argv[1]

#Dish Extraction
f_dict = open('data/restaurant_dict_list/restaurant_dict_%s.json'%rest_num)
rest_dict = json.load(f_dict)
menu = [dish for dish in rest_dict['menu'] if dish['mentioned_review_num'] >= 10]
new_menu = []
for dish in menu:
    dish['length'] = len(dish['name'])
    new_menu.append(dish)
new_menu = sorted(new_menu, key=itemgetter('length'), reverse=True)
menu = new_menu

menu_length = len(menu)
num1, num2 = int(menu_length*0.27), int(menu_length*0.74)

dish_list = []
for num in random.sample(range(0, num1), 3):
    dish_list.append(menu[num])

for num in random.sample(range(num1, num2), 4):
    dish_list.append(menu[num])

for num in random.sample(range(num2, menu_length), 3):
    dish_list.append(menu[num])

f_review = open('data/frontend_reviews/restaurant_%s.json'%rest_num)
dic = json.load(f_review)
dishes_reviews = dic['dish_reviews']

for dish in dish_list:
    dish_name = dish['name']
    dish_ar = dish['name_ar']
    dish_reviews = []
    for d in dishes_reviews:
        if d['dish_name'] == dish_name:
            dish_reviews = d['reviews']
    dish_reviews = [review.replace('\n','') for review in dish_reviews]
    dish_reviews = sorted(dish_reviews, key=len)
    dish_reviews = [unicodedata.normalize('NFKD', review).encode('ASCII', 'ignore') for review in dish_reviews]
    dish_reviews = [review.replace('<mark>'+dish['name']+'</mark>','@@@@@'+dish['name']+'@@@@@') for review in dish_reviews]
    dish_reviews = [review.replace('<mark>','').replace('</mark>','') for review in dish_reviews]

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
        extract_reviews.append(dish_reviews[num])
    f_out = open('data/QuestionReviews/rest%s/%s.txt'%(rest_num, dish_ar),'w+')
    f_out.write('\n'.join(extract_reviews))

