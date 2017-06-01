# -*- coding: utf8 -*-
import csv
import sys

class FleissKappa:
    def __init__(self):
        self.f = open('1A.csv')
        self.raw = [line[2:] for line in [line for line in csv.reader(self.f)][1:]]
        self.data = []
        for col in range(0,len(self.raw[0])):
            lst = [int(row[col]) for row in self.raw]
            cnt_lst = []
            for i in range(0,5):
                cnt_lst.append(lst.count(i+1))
            self.data.append(cnt_lst)

        new = []
        for r in self.data:
            lst = []
            lst.append(r[0]+r[1])
            lst.append(r[2])
            lst.append(r[3]+r[4])
            new.append(lst)
        self.data = new

    def calculate(self):
        N = float(len(self.data))
        n = float(sum(self.data[0]))
        k = float(len(self.data[0]))

        p_j = []
        for i in range(int(k)):
            p_j.append(sum([r[i] for r in self.data])/(N*n))
        P_e_mean = sum(n*n for n in p_j)

        P_i = []
        for i in range(int(N)):
            P_i.append((sum(n*n for n in self.data[i])-n)/(n*(n-1)))
        P_mean = sum(P_i)/N

        kappa = (P_mean - P_e_mean)/(1.0-P_e_mean)
        print kappa


if __name__ == "__main__":
    kappa = FleissKappa()
    kappa.calculate()

