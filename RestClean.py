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
    else:
        new_business_list.append(rest)
i = 1
for rest in new_business_list:
    rest["index"] = i
    i+=1

f = open("data/new_business_list.json","w+")
f.write(json.dumps(new_business_list, indent = 4))
