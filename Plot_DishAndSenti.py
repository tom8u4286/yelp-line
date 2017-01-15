import matplotlib
import matplotlib.pyplot as plt
import re, sys, json


class Plot_DishAndSenti:

    def __init__(self):
        """src == '../data/line-data/vectors/2dim/restaurant_1_vector2.json'"""
        self.src = sys.argv[1]
        self.rest_num = int(re.search("_([0-9]+)_",sys.argv[1].split("/")[5]).group(1))
        print self.rest_num

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
                plt.text( vec[0]+0.01, vec[1]+0.01, word)
            elif "_" in word:
                print word
                ax.plot( vec[0], vec[1], "yo")
                plot.text( vec[0]+0.01, vec[1]+0.01, word)
        ax.set_title("dish and Senti")
        plt.savefig("Dish_and_Senti.png")



if __name__ == "__main__":
    plot = Plot_DishAndSenti()
    plot.render()
