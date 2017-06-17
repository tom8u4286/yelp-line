# -*- coding: utf8 -*-
import csv
import sys
from sklearn.metrics import cohen_kappa_score

class FleissKappa:
    def __init__(self):
        self.f = open('data/QuestionResult/1A.csv')
        self.raw = [line[2:] for line in [line for line in csv.reader(self.f)][1:]]
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

        self.data = self.data[45:][:5]
        tmp = []
        self.data = [[int(n) for n in l] for l in self.data]
        self.data1 = [5, 4, 3,5,2,5, 5, 5, 4]
        self.data2 = [5, 4, 3,5,2,5, 5, 4, 5]
        print cohen_kappa_score(self.data1,self.data2)
        sys.exit()

        for l in self.data:
            print l

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

