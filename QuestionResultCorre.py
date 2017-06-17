# -*- coding: utf8 -*-
import csv
import sys
from scipy.stats.stats import pearsonr

class FleissKappa:
    def __init__(self):
        self.rest_num = sys.argv[1]
        self.f = open('data/QuestionResult/%sA.csv'%self.rest_num)
        self.raw = [line[2:] for line in [line for line in csv.reader(self.f)][1:]]
        print pearsonr([int(n) for n in self.raw[0]],[int(n) for n in self.raw[1]])
        print pearsonr([int(n) for n in self.raw[0]],[int(n) for n in self.raw[2]])
        print pearsonr([int(n) for n in self.raw[1]],[int(n) for n in self.raw[2]])
        sys.exit()
        self.data = []
        for col in range(0,len(self.raw[0])):
            lst = [int(row[col]) for row in self.raw]
            cnt_lst = []
            for i in range(0,5):
                cnt_lst.append(lst.count(i+1))
            self.data.append(cnt_lst)

       # new = []
       # for r in self.data:
       #     lst = []
       #     lst.append(r[0]+r[1])
       #     lst.append(r[2])
       #     lst.append(r[3]+r[4])
       #     new.append(lst)
       # self.data = new

        self.data = self.data
        tmp = []
        self.data = [[int(n) for n in l] for l in self.data]
        #self.data = [[0,0,0,0,3],[0,0,0,0,3],[0,0,0,0,3],[0,0,0,0,3],[0,0,0,1,2]]
        for l in self.data:
            print l
        sys.exit()

    def calculate(self):
        N = float(len(self.data))
        n = float(sum(self.data[0]))
        k = float(len(self.data[0]))
        print 'N:',N,' n:', n,' k:', k

        p_j = []
        for i in range(int(k)):
            p_j.append(sum([r[i] for r in self.data])/(N*n))
        print 'p_j:',p_j
        P_e_mean = sum([num*num for num in p_j])
        print 'P_e_mean:',P_e_mean

        P_i = []
        for i in range(int(N)):
            P_i.append(float(sum([num*num for num in self.data[i]])-n)/float(n*(n-1)))
        print 'P_i:',P_i
        P_mean = sum(P_i)/N
        print 'P_mean:',P_mean

        kappa = (P_mean - P_e_mean)/(1.0-P_e_mean)
        print 'kappa:',kappa


if __name__ == "__main__":
    kappa = FleissKappa()
    kappa.calculate()

