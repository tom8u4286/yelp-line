import matplotlib
import matplotlib.pyplot as plt
import sys, json


class Plot_DishAndSenti:

    def __init__(self):
        """src == '../data/line-data/vectors/2dim/restaurant_1_vector2.json'"""
        self.rest_num = sys.argv[1]
        self.build_type = sys.argv[2]
        self.src = "data/vectors/2dim/restaurant_%s_vector2_type%s.json"%(self.rest_num, self.build_type)
        #self.rest_num = int(re.search("_([0-9]+)_",sys.argv[1].split("/")[5]).group(1))

    def render(self):
        dic = json.load(open(self.src))

        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.set_xlim( -1, 1)
        ax.set_ylim( -1, 1)

        for word in dic:
            vec = word["vector2"]
            word = word["word"]
            if "_senti" in word:
                ax.plot( vec[0], vec[1], "b+")
                plt.text( vec[0]+0.0001, vec[1]+0.0001, word.strip("_senti"))
            elif "_" in word:
                print word
                ax.plot( vec[0], vec[1], "yo")
                plt.text( vec[0]+0.0001, vec[1]+0.0001, word.strip("_mon-ami-gabi"))
        ax.set_title("rest%s, type%s"%(self.rest_num,self.build_type))
        plt.show()
        plt.savefig("data/plot/restaurant_%s_type%s.png"%(self.rest_num, self.build_type))
        self.rest_num = sys.argv[1]



if __name__ == "__main__":
    plot = Plot_DishAndSenti()
    plot.render()
