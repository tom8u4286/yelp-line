import json
import sys
from os import listdir
total_reviews_count = 0
avg_word_count_pre_review = 0
avg_menu_length = 0
avg_senti_per_review = 0
dish_senti_avg_length = 0
voc_sizes = []

rawReviewsFileNames =[f for f in listdir('data/reviews/') if 'restaurant_' in f]
fileNum = len(rawReviewsFileNames)

for i in range(1,fileNum+1):
    f_dic = open('data/restaurant_dict_list/restaurant_dict_%s.json'%i)
    rest_dic = json.load(f_dic)
    total_reviews_count += rest_dic['review_count']
    avg_word_count_pre_review += rest_dic['avg_word_count_pre_review']
    avg_menu_length += rest_dic['menu_length']
    avg_senti_per_review += rest_dic['senti_per_review']
    dish_senti_avg_length += rest_dic['dish_senti_avg_len']
    f_voc = open('data/voc/restaurant_%s_voc.txt'%i)
    voc_size = sum(1 for l in f_voc)
    voc_sizes.append(voc_size)

print 'restaurant amount: ', fileNum
print 'avg_menu_length: ',float(avg_menu_length)/fileNum
print 'total reviews count: ',total_reviews_count
print 'avg reviews count per rest: ',float(total_reviews_count)/fileNum
print 'vocabularty size per rest: ',float(sum(voc_sizes))/fileNum
print 'avg_word_count_pre_review: ',float(avg_word_count_pre_review)/fileNum
print 'avg_senti_per_review: ',float(avg_senti_per_review)/fileNum
print 'dish_senti_avg_length: ',float(dish_senti_avg_length)/fileNum
