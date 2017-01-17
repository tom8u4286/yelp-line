import json, sys
#import xlwt
import xlsxwriter
rest_num = sys.argv[1]

f1 = open("data/rank/restaurant_%s_rank_type1.json"%rest_num )
f2 = open("data/rank/restaurant_%s_rank_type2.json"%rest_num )
f3 = open("data/rank/restaurant_%s_rank_type3.json"%rest_num )
f4 = open("data/rank/restaurant_%s_rank_type4.json"%rest_num )
dic1 = json.load(f1)
dic2 = json.load(f2)
dic3 = json.load(f3)
dic4 = json.load(f4)
dic_list = [dic1, dic2, dic3, dic4]

book = xlsxwriter.Workbook("test.xls")
sh1 = book.add_worksheet("sheet1")

sh1.write("A3", "higher0")
sh1.write("A4", "higher0.2")
sh1.write("A5", "higher0.4")
sh1.write("A6", "higher0.6")
sh1.write("A7", "higher0.8")
sh1.write("A8", "avg")
sh1.merge_range('B1:D1', 'Method 1')
sh1.merge_range('E1:G1', 'Method 2')
sh1.merge_range('H1:J1', 'Method 3')
sh1.merge_range('K1:M1', 'Method 4')

i = 1
while i<12:
    for j in range(1,4):
        sh1.write(1,i,"@%s0"%j)
        i+=1

col = 1
for dic in dic_list:
    row = 2
    for higher in ["0","02","04","06","08"]:
        sh1.write(row,col,dic["precision_higher%s"%higher]["at10"])
        sh1.write(row,col+1,dic["precision_higher%s"%higher]["at20"])
        sh1.write(row,col+2,dic["precision_higher%s"%higher]["at30"])
        row+=1
    sh1.write(row,col,dic["precision_avg"]["at10"])
    sh1.write(row,col+1,dic["precision_avg"]["at20"])
    sh1.write(row,col+2,dic["precision_avg"]["at30"])
    col+=3


#book.save("test.xls")
book.close()


