import json
total_reviews_count = 0
avg_word_count_pre_review = 0
avg_menu_length = 0
avg_senti_per_review = 0
dish_senti_avg_length = 0


for i in range(1,265):
    if i == 206:
        continue
    f_dic = open('data/restaurant_dict_list/restaurant_dict_%s.json'%i)
    rest_dic = json.load(f_dic)
    total_reviews_count += rest_dic['review_count']
    avg_word_count_pre_review += rest_dic['avg_word_count_pre_review']
    avg_menu_length += rest_dic['menu_length']
    avg_senti_per_review += rest_dic['senti_per_review']
    dish_senti_avg_length += rest_dic['dish_senti_avg_len']

print 'total reviews count: ',total_reviews_count
print 'avg_word_count_pre_review: ',float(avg_word_count_pre_review)/264
print 'avg_menu_length: ',float(avg_menu_length)/264
print 'avg_senti_per_review: ',float(avg_senti_per_review)/264
print 'dish_senti_avg_length: ',float(dish_senti_avg_length)/264
