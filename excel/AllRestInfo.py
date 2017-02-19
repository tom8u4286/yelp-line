import json
#import xlwt
import xlsxwriter
#rest_num = sys.argv[1]

book = xlsxwriter.Workbook("AllRestInfo.xlsx")
sh1 = book.add_worksheet("AllRest")

offset = 0
col = 2
sh1.write( 1, 1, "rest_name")
sh1.write( 1, 2, "review_count")
sh1.write( 1, 3, "menu_length")
sh1.write( 1, 4, "senti_per_review")
sh1.write( 1, 5, "dish_senti_avg_len")

for r in range(1,21):
    rest_num = r
    f_rest_dic = open("../data/restaurant_dict_list/restaurant_dict_%s.json"%rest_num )
    rest_dic = json.load(f_rest_dic)

    sh1.write(col, 0, "rest%s"%rest_num)
    sh1.write(col, 1, rest_dic["restaurant_name"])
    sh1.write(col, 2, rest_dic["review_count"])
    sh1.write(col, 3, rest_dic["menu_length"])
    sh1.write(col, 4, rest_dic["senti_per_review"])
    sh1.write(col, 5, rest_dic["dish_senti_avg_len"])
    col+=1

book.close()


