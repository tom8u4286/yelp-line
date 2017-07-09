from scipy.stats.stats import pearsonr
import sys
import csv

class ResultCorrelation:
    def __init__(self):
        #data1 = [3,5,5,5,5]
        #data2 = [5,5,5,4,5]
        #data3 = [5,4,5,4,5]
        self.rest_num = sys.argv[1]
	self.f = open('data/QuestionResult/%sA.csv'%self.rest_num)
        self.raw = [line[2:] for line in [line for line in csv.reader(self.f)][1:]]
        self.data = []
        for col in range(0,len(self.raw[0])):
            lst = [int(row[col]) for row in self.raw]
            cnt_lst = []
            for i in range(0,5):
                cnt_lst.append(lst.count(i+1))
            self.data.append(cnt_lst)
	data1 = [int(n) for n in self.raw[0]]
	data2 = [int(n) for n in self.raw[1]]
	data3 = [int(n) for n in self.raw[2]]

        co1  = pearsonr(data1,data2)[0]
        co2  = pearsonr(data1,data3)[0]
        co3  = pearsonr(data2,data3)[0]

        print 'Average:', (co1+co2+co3)/3.0
        #m = len(data1)
        #n = 3
        #R1 = sum(data1)
        #R2 = sum(data2)
        #R3 = sum(data3)
        #R_h = float(R1+R2+R3)/3.0
        #S = (R1-R_h)*(R1-R_h) + (R2-R_h)*(R2-R_h) + (R3-R_h)*(R3-R_h)
        #W = float(12*S)/float(m*m*(n*n*n - n))
        #print W


if __name__ == '__main__':
    cor = ResultCorrelation()
