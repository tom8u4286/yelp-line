'''
This program aims to render the example for paper, which has 2 or 3 overlap dishes in the frq top5 and proposed method top5.
'''
import json
import sys
from collections import OrderedDict
from operator import itemgetter
from os import listdir

restFileList = [f for f in listdir('data/reviews/') if 'restaurant_' in f]
fileNum = len(restFileList)

extractedRest = []
for num in range(1,fileNum+1):
    f = open('data/rank/restaurant_%s_rank_type3.json'%num)
    dic = json.load(f)
    dishes = dic['rank']

    overlap_num = 0
    for dish in dishes[:5]:
        if dish['rank_by_sum_higher0_cos_zXnorm_frq'] < 6:
            overlap_num +=1

    if overlap_num == 2 or overlap_num == 3:
        proposedDishes = [dish for dish in dishes if dish['rank_by_sum_higher0_cos_zXnorm_frq'] < 6 ]
        if len(proposedDishes) != 5:
            print 'less than 5:', num
            continue
        if proposedDishes[0]['dish_cnt'] > 10 and proposedDishes[1]['dish_cnt'] > 10:
            if proposedDishes[2]['dish_cnt'] > 10 and proposedDishes[3]['dish_cnt'] > 10:
                if proposedDishes[4]['dish_cnt'] > 10:
                    continue

        frqDishes = []
        for dish in dishes[:5]:
            newDish = OrderedDict()
            newDish['dish'] = dish['dish']
            newDish['frq'] = dish['dish_cnt']
            newDish['rank_by_frq'] = dish['rank_by_frq']
            newDish['rank_by_proposed_method'] = dish['rank_by_sum_higher0_cos_zXnorm_frq']
            frqDishes.append(newDish)

        proposedDishes = []
        for dish in sorted([dish for dish in dishes if dish['rank_by_sum_higher0_cos_zXnorm_frq'] < 6 ],key = itemgetter('rank_by_sum_higher0_cos_zXnorm_frq')):
            newDish = OrderedDict()
            newDish['dish'] = dish['dish']
            newDish['frq'] = dish['dish_cnt']
            newDish['rank_by_frq'] = dish['rank_by_frq']
            newDish['rank_by_proposed_method'] = dish['rank_by_sum_higher0_cos_zXnorm_frq']
            proposedDishes.append(newDish)

        f_dict = open('data/restaurant_dict_list/restaurant_dict_%s.json'%num)
        restName = json.load(f_dict)['restaurant_name']
        restDict = OrderedDict()
        restDict['rest_num'] = num
        restDict['rest_name'] = restName
        restDict['frq_top5'] = frqDishes
        restDict['proposed_top5'] = proposedDishes
        extractedRest.append(restDict)

f_out = open('extractedRestWithOverlap.json','w+')
f_out.write(json.dumps(extractedRest, indent=4))

