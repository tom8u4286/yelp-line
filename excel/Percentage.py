import json
#import xlwt
import xlsxwriter
#rest_num = sys.argv[1]

book = xlsxwriter.Workbook("Percentage.xlsx")
sh1 = book.add_worksheet("@10")

offset = 0
col = 2
sh1.write( 1, 1, "higher0Xfrq")
sh1.write( 1, 2, "higher0Xnfrq")
sh1.write( 1, 3, "higher0zXnfrq")
sh1.write( 1, 4, "z_top5")
sh1.write( 1, 5, "z_top10")

for r in range(1,21):
    rest_num = r
    f_rest_dic = open("../data/rank/restaurant_%s_rank_type3.json"%rest_num )
    rest_dic = json.load(f_rest_dic)

    sh1.write(col, 0, "rest%s"%rest_num)
    sh1.write(col, 1, rest_dic["percentage_higher0_cosXfrq"]["at10"])
    sh1.write(col, 2, rest_dic["percentage_higher0_cosXnorm_frq"]["at10"])
    sh1.write(col, 3, rest_dic["percentage_higher0_cos_z_Xnorm_frq"]["at10"])
    sh1.write(col, 4, rest_dic["percentage_higher0_cos_z_top5"]["at10"])
    sh1.write(col, 5, rest_dic["percentage_higher0_cos_z_top10"]["at10"])
    col+=1

book.close()


