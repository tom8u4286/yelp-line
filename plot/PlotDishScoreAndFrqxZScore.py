import json, sys, uuid, os
import numpy as np
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict

class PlotDishScoreAndSentiCosVar:

    def __init__(self):
        self.vec64_src = "../data/vectors/norm_64dim/norm_restaurant_%s_vector64_type%s.txt"%(sys.argv[1],sys.argv[2])
        #self.rest_num = int(re.search("_([0-9]+)_", sys.argv[1].split("/")[3]).group(1))
        self.rest_num = sys.argv[1]
        #self.build_type = int(re.search("type([0-9]+)", sys.argv[1].split("/")[3]).group(1))
        self.build_type = sys.argv[2]
        self.senti_file_src = "../data/frontend_sentiment/frontend_sentiment_rest%s.json"%self.rest_num
        #self.rest_dic_src ="../data/restaurant_dict_list/restaurant_dict_list.json"
        self.rest_dic_src = "../data/restaurant_dict_list/restaurant_dict_%s.json"%self.rest_num
        self.rest_dic = {}

    def get_words_and_vectors(self):
        words = []
        vectors = []
        f_vec64 = open(self.vec64_src)
        length = int(next(f_vec64).split(" ")[0])
        for line in f_vec64:
            word_vec = line.split(" ")
            words.append(word_vec[0])
            vec = [float(num) for num in word_vec[1:-1]]
            vectors.append(vec)
        return words, vectors

    def get_rest_name(self):
        f_res_dic = open(self.rest_dic_src)
        rest_dic = json.load(f_res_dic)
        rest_name = rest_dic["restaurant_name"]
        #for rest in rest_dic:
        #    if rest["index"] == self.rest_num:
        #        rest_name = rest["restaurant_name"]
        return rest_name

    def get_indices(self, words, vectors):
        senti_indices = []
        dish_indices = []
        rest_name = self.get_rest_name().lower().replace(" ","-").replace("&", "and").replace("\'", "").replace(".", "").replace(",","")
        stemmer = SnowballStemmer('english')
        rest_name = stemmer.stem(rest_name)
        #print "rest name:",rest_name
        for idx, word in enumerate(words):
            if "_senti" in word:
                senti_indices.append(idx)
            elif rest_name in word:
                dish_indices.append(idx)
        return senti_indices, dish_indices

    def get_senti_dic_list(self):
        f = open(self.senti_file_src)
        senti_dic = json.load(f)
        return senti_dic

    def plot(self):
        words, vectors = self.get_words_and_vectors()
        senti_indices, dish_indices = self.get_indices(words, vectors)
        #print senti_indices, dish_indices
        #sys.exit("stop61")
        senti_dic_list = self.get_senti_dic_list()
        rest_name = self.get_rest_name()
        A = np.array(vectors)
        cos_matrix = cosine_similarity(A)

        matplotlib.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        ax.set_title("rest%s: "%self.rest_num+rest_name)
        ax.set_xlabel('score(sum of senti higher than 0.5)')
        ax.set_ylabel('z-score*norm(frq)(senti higher than 0.5)')

        for dish_index in dish_indices:
            cos_list = []
            senti_words_list = []
            total_frq_of_senti = 0
            for senti_index in senti_indices:
                if cos_matrix[dish_index][senti_index] > 0.5 :
                    cos_list.append(cos_matrix[dish_index][senti_index] )
                    senti_words_list.append(words[senti_index])
                    for senti in senti_dic_list:
                        if words[senti_index] == senti["word"]:
                            total_frq_of_senti += senti["count"]
            #print cos_list
            #print senti_words_list
            #sys.exit("stop81")
            #zscore_list = stats.zscore(np.array(cos_list)).tolist()
            #avg_zscore = float(sum(zscore_list))/float(len(zscore_list))
            norm_total_frq_of_senti = float(total_frq_of_senti) / float(max([senti["count"] for senti in senti_dic_list]))
            score = sum(cos_list)
            ax.plot(score, norm_total_frq_of_senti, 'bo')

        plt.savefig("../data/plot/DishScoreAndFrqxZScore/restaurant_%s_DishScoreAndFrqxZScore.png"%self.rest_num)
        #plt.show()

class NoIndent(object):
    def __init__(self, value):
        self.value = value

class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result

if __name__ == "__main__":
    plotDish = PlotDishScoreAndSentiCosVar()
    plotDish.plot()
