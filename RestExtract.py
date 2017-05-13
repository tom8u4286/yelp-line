'''
This program aims to extract the restaurants which are located in Las Vegas from business_list.json,
released by Yelp Data Challenge.
'''
import sys
import json
from collections import OrderedDict

business_list = json.load(open("data/business_list.json"))
new_business_list = []
#remove_list = [2, 46, 49, 118, 377, 392, 491, 446, 484]

for rest in business_list:
    #if rest["index"] in remove_list or rest['city'] != 'Las Vegas':
    if rest['city'] != 'Las Vegas':
        continue
    if rest['business_name'] == 'Tryst Nightclub':
        continue
    if rest['business_name'] == 'Egg Works':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == 'Japanese Curry Zen':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == 'Original Lindo Michoacan':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == 'Chin Chin':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == 'Egg Works':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == "Chang's Hong Kong Cuisine":
        #Egg Works only has three dishes whose frq is more than 5
        continue
    if rest['business_name'] == 'Buldogis Gourmet Hot Dogs':
        #Egg Works only has three dishes whose frq is more than 5
        continue
    else:
        new_business_list.append(rest)
i = 1
for rest in new_business_list:
    rest["index"] = i
    i+=1

f = open("data/new_business_list.json","w+")
f.write(json.dumps(new_business_list, indent = 4))
