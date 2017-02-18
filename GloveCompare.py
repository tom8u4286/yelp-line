import json
#import xlwt
import xlsxwriter
#rest_num = sys.argv[1]

book = xlsxwriter.Workbook("test.xlsx")
sh1 = book.add_worksheet("sheet1")

offset = 0
for r in range(1,500):
    rest_num = r
    try:
        f1 = open("data/rank/restaurant_%s_rank_type1.json"%rest_num )
        f2 = open("data/rank/restaurant_%s_rank_type2.json"%rest_num )
        f3 = open("data/rank/restaurant_%s_rank_type3.json"%rest_num )
        f4 = open("data/rank/restaurant_%s_rank_type4.json"%rest_num )
    except:
        print "cannot open file: rest%s"%(r)
        continue
    dic1 = json.load(f1)
    dic2 = json.load(f2)
    dic3 = json.load(f3)
    dic4 = json.load(f4)
    dic_list = [dic1, dic2, dic3, dic4]

    sh1.write( 2 + offset, 0, "higher0")
    sh1.write( 3 + offset, 0, "higher0.2")
    sh1.write( 4 + offset, 0, "higher0.4")
    sh1.write( 5 + offset, 0, "higher0.6")
    sh1.write( 6 + offset, 0, "higher0.8")
    sh1.write( 7 + offset, 0, "avg")
    sh1.merge_range( 0 + offset, 1, 0 + offset, 3, 'Method 1')
    sh1.merge_range( 0 + offset, 4, 0 + offset, 6, 'Method 2')
    sh1.merge_range( 0 + offset, 7, 0 + offset, 9, 'Method 3')
    sh1.merge_range( 0 + offset, 10, 0 + offset, 12, 'Method 4')
    sh1.merge_range( 0 + offset, 0, 1 + offset, 0,'rest%s'%rest_num)

    i = 1
    while i<12:
        for j in range(1,4):
            sh1.write(1 + offset,i,"@%s0"%j)
            i+=1

    col = 1
    for dic in dic_list:
        row = 2
        for higher in ["0","02","04","06","08"]:
            sh1.write(row + offset, col, dic["precision_higher%s"%higher]["at10"])
            sh1.write(row + offset, col+1, dic["precision_higher%s"%higher]["at20"])
            sh1.write(row + offset, col+2, dic["precision_higher%s"%higher]["at30"])
            row+=1
        sh1.write(row + offset, col, dic["precision_avg"]["at10"])
        sh1.write(row + offset, col+1, dic["precision_avg"]["at20"])
        sh1.write(row + offset, col+2, dic["precision_avg"]["at30"])
        col+=3
    offset += 10


#book.save("test.xls")
book.close()


