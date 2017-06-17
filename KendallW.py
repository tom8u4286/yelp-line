from scipy.stats.stats import pearsonr

class KendallW:
    def __init__(self):
        data1 = [3,5,5,5,5]
        data2 = [5,5,5,4,5]
        data3 = [5,4,5,4,5]
        print pearsonr(data2,data3)
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
    kendall = KendallW()
