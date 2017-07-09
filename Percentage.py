import json
import sys

class Percentage:
    '''This program aims to calculate the percentage of the ranking result
    overlaps the result of frequency.'''
    def __init__(self):
        self.atFive = 0
        self.atTen = 0
        self.atTwen = 0
        for i in range(1,257):
            if i == 141:
                continue
            f = open('data/rank/restaurant_%s_rank_type3.json'%i)
            dic = json.load(f)
            at5 = dic['percentage_higher0_cosXfrq']['at5']
            at10 = dic['percentage_higher0_cosXfrq']['at10']
            at20 = dic['percentage_higher0_cosXfrq']['at20']
            self.atFive += at5
            self.atTen += at10
            self.atTwen += at20

        print 'proposed method:'
        print '@5:',float(self.atFive)/255.0
        print '@10:',float(self.atTen)/255.0
        print '@20:',float(self.atTwen)/255.0

        self.atFive = 0
        self.atTen = 0
        self.atTwen = 0
        for i in range(1,257):
            if i == 141:
                continue
            f = open('data/rank/restaurant_%s_rank_type3.json'%i)
            dic = json.load(f)
            at5 = dic['percentage_sum_senti_coo']['at5']
            at10 = dic['percentage_sum_senti_coo']['at10']
            at20 = dic['percentage_sum_senti_coo']['at20']
            self.atFive += at5
            self.atTen += at10
            self.atTwen += at20

        print 'coo:'
        print '@5:',float(self.atFive)/255.0
        print '@10:',float(self.atTen)/255.0
        print '@20:',float(self.atTwen)/255.0

        self.atFive = 0
        self.atTen = 0
        self.atTwen = 0
        for i in range(1,257):
            if i == 141:
                continue
            f = open('data/rank/restaurant_%s_rank_type3.json'%i)
            dic = json.load(f)
            at5 = dic['percentage_avg']['at5']
            at10 = dic['percentage_avg']['at10']
            at20 = dic['percentage_avg']['at20']
            self.atFive += at5
            self.atTen += at10
            self.atTwen += at20

        print 'avg:'
        print '@5:',float(self.atFive)/255.0
        print '@10:',float(self.atTen)/255.0
        print '@20:',float(self.atTwen)/255.0
if __name__ =='__main__':
    per = Percentage()

