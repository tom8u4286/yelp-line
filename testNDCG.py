import json
from operator import itemgetter
f = open('restaurant_1_rank_type3.json')

rank_dic = json.load(f)
dish_list = rank_dic['rank']

top_list = []
for num in range(1,6):
    for dish in dish_list:
        if dish['rank_by_frq'] == num or dish['rank_by_sum_higher0_cos_zXnorm_frq'] == num:
            top_list.append(dish['dish'])

lst = []
for dish in dish_list:
    for item in top_list:
        if dish['dish'] == item:
            dic = {}
            dic['dish'] = dish['dish']
            dic['rank_by_sum_higher0_cos_zXnorm_frq'] = dish['rank_by_sum_higher0_cos_zXnorm_frq']
            lst.append(dic)
lst = sorted(lst, key=itemgetter('rank_by_sum_higher0_cos_zXnorm_frq'))
for i in lst:
    print i


ground_truth = ['baguette_mon-ami-gabi','grilled-pork-tenderloin_mon-ami-gabi','salmon-spinach-and-baby-kale-salad_mon-ami-gabi','chicken-grand-mere_mon-ami-gabi','ratatouille_mon-ami-gabi','salmon_mon-ami-gabi','steak-frites_mon-ami-gabi','mac-cheese_mon-ami-gabi','french-onion-soup_mon-ami-gabi','frites_mon-ami-gabi']

ndcg = [4,4,3,3,2,2,1,1,0,0]
count = 0
for d, o, score in zip(ground_truth, lst, ndcg):
    #print d , o['dish']
    if d == o['dish']:
        count += score
print 'ndcg: ', float(count)/ float(sum(ndcg))



