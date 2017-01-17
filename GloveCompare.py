import json, sys
import xlwt
rest_num = sys.argv[1]

f1 = open("data/rank/restaurant_%s_rank_type1.json"%rest_num )
f2 = open("data/rank/restaurant_%s_rank_type2.json"%rest_num )
f3 = open("data/rank/restaurant_%s_rank_type3.json"%rest_num )
f4 = open("data/rank/restaurant_%s_rank_type4.json"%rest_num )

dic1 = json.load(f1)
dic2 = json.load(f2)
dic3 = json.load(f3)
dic4 = json.load(f4)
