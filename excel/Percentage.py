import json
#import xlwt
import xlsxwriter
#rest_num = sys.argv[1]

book = xlsxwriter.Workbook("Percentage.xlsx")
sh1 = book.add_worksheet("@10")
sh2 = book.add_worksheet("@20")
sh3 = book.add_worksheet("@30")
format1 = book.add_format({'font_color': '#FF0000'})
sh_list = [sh1,sh2,sh3]
at_list = ["at10","at20","at30"]
for sheet, at in zip(sh_list,at_list):
    for i in range(1,23):
        sheet.conditional_format('B%s:F%s'%(i,i), {'type': 'top','value': 1,"format":format1})
    #sheet.write( 1, 1, "higher0Xfrq")
    sheet.write( 1, 0, "percent")
    #sheet.write( 1, 1, "higher0Xfrq")
    sheet.write( 1, 1, "higher0Xnfrq")
    sheet.write( 1, 2, "higher0zXnfrq")
    #sheet.write( 1, 4, "z_top5")
    #sheet.write( 1, 5, "z_top10")
    sheet.write( 1, 3, "cos_avg")
    sheet.write( 1, 4, "cos_max_1")
    sheet.write( 1, 5, "cos_sum_total(bl2)")
    #sheet.write( 1, 7, "sum_higher0")
    #sheet.write( 1, 8, "sum_higher05")
    sheet.write( 1, 7, "review_count")
    sheet.write( 1, 8, "menu_length")
    sheet.write( 1, 9, "senti_per_review")
    sheet.write( 1, 10, "dish_senti_avg_len")

    offset = 0
    col = 2

    for r in range(1,21):
        rest_num = r
        f_rest_dic = open("../data/rank/restaurant_%s_rank_type3.json"%rest_num )
        rest_rank_dic = json.load(f_rest_dic)
        f_rest_dic = open("../data/restaurant_dict_list/restaurant_dict_%s.json"%rest_num )
        rest_dic = json.load(f_rest_dic)

        sheet.write(col, 0, "rest%s"%rest_num)
        #sheet.write(col, 1, rest_rank_dic["percentage_higher0_cosXfrq"][at])
        sheet.write(col, 1, rest_rank_dic["percentage_higher0_cosXnorm_frq"][at])
        sheet.write(col, 2, rest_rank_dic["percentage_higher0_cos_z_Xnorm_frq"][at])
        sheet.write(col, 3, rest_rank_dic["percentage_avg"][at])
        sheet.write(col, 4, rest_rank_dic["percentage_max_1"][at])
        sheet.write(col, 5, rest_rank_dic["percentage_sum_total"][at])
        #sheet.write(col, 4, rest_rank_dic["percentage_higher0_cos_z_top5"][at])
        #sheet.write(col, 5, rest_rank_dic["percentage_higher0_cos_z_top10"][at])
        #sheet.write(col, 6, rest_rank_dic["percentage_avg"][at])
        #sheet.write(col, 7, rest_rank_dic["percentage_higher0"][at])
        #sheet.write(col, 8, rest_rank_dic["percentage_higher05"][at])
        sheet.write(col, 6, "rest%s"%rest_num)
        sheet.write(col, 7, rest_dic["review_count"])
        sheet.write(col, 8, rest_dic["menu_length"])
        sheet.write(col, 9, rest_dic["senti_per_review"])
        sheet.write(col, 10, rest_dic["dish_senti_avg_len"])
        col+=1

book.close()


