import json, sys, uuid, os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import scipy.stats as stats
import re
from collections import OrderedDict

class DishScore:

    def __init__(self):

        """sys.argv[0] ../data/line-data/vectors/200dim/restaurant_1_vector200.txt"""
        """sys.argv[0] data/vectors/200dim/restaurant_1_vector200.txt"""
        self.vec64_src = sys.argv[1]
        self.rest_num = int(re.search("_([0-9]+)_", sys.argv[1].split("/")[3]).group(1))
        self.rest_dic_src ="data/restaurant_dict_list/restaurant_dict_list.json"
        self.rest_dic_list_src = "data/restaurant_dict_list/restaurant_dict_%s.json"%self.rest_num
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
        rest_name = ""
        for rest in rest_dic:
            if rest["index"] == self.rest_num:
                rest_name = rest["restaurant_name"]
        return rest_name

    def get_indices(self, words, vectors):
        senti_indices = []
        dish_indices = []
        rest_name = self.get_rest_name().lower().replace(" ","-")
        print "rest name:",rest_name
        for idx, word in enumerate(words):
            if "_senti" in word:
                senti_indices.append(idx)
            elif rest_name in word:
                dish_indices.append(idx)
        return senti_indices, dish_indices

    def calculate(self):
        """2017/12/18 Tom"""
        """Render the cosine matrix."""
        words, vectors = self.get_words_and_vectors()
        senti_indices, dish_indices = self.get_indices(words, vectors)
        A = np.array(vectors)
        cos_matrix = cosine_similarity(A)

        dish_list = []
        for dish_index in dish_indices:
            dic = {}
            dic["dish"] = words[dish_index]
            avg_cos = sum( [cos_matrix[dish_index][senti_index] for senti_index in senti_indices] )/len(senti_indices)
            max_cos_10 = sorted( [cos_matrix[dish_index][senti_index] for senti_index in senti_indices], reverse=True )[:10]
            max_words = [words[ list(cos_matrix[dish_index]).index(max_cos) ] for max_cos in max_cos_10]
            dic["avg_cos"] = avg_cos
            dic["max_cos_10"] = max_cos_10
            dic["max_words"] = max_words
            dish_list.append(dic)

        return dish_list

    def rank(self, dish_list):

        #rank by frquency
        # 1/2 added by Tom
        f = open( self.rest_dic_list_src )
        rest_dict_list = json.load(f)
        menu = rest_dict_list["menu"]
        for i in range(0, len(dish_list)):
            dish_cnt = 0
            for dish in menu:
                if dish_list[i]["dish"] == dish["name_ar"]:
                    dish_cnt = dish["count"]
                    break
            dish_list[i]["dish_cnt"] = dish_cnt

        dish_list = sorted(dish_list, key=lambda k: k['max_cos_10'][:1], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_max"] = i+1

        rank_by_max = dish_list

        dish_list = sorted(dish_list, key=lambda k: k['avg_cos'], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_avg"] = i+1

        rank_by_avg = dish_list


        # calculate stats.kendalltau
        rank_by_avg_top10 = dish_list[:5]
        rank_by_avg_top10 = sorted(rank_by_avg_top10, key=lambda k: k['dish_cnt'], reverse=True)
        for i in range(0, len(rank_by_avg_top10)):
            rank_by_avg_top10[i]["rank_by_cnt"] = i+1
        rank_by_cnt_top10 = rank_by_avg_top10
        cnt_rank = [dish["rank_by_cnt"] for dish in rank_by_cnt_top10]
        avg_rank = [dish["rank_by_avg"] for dish in rank_by_cnt_top10]
        #print cnt_rank
        #print avg_rank
        tau, p_value = stats.kendalltau(cnt_rank, avg_rank)
        f_test = open("test.json","w+")
        dic = {}
        dic["kendalltau_avg_frq"] = tau
        ordered_dict_list = []
        for item in rank_by_cnt_top10:
            ordered_dict = OrderedDict()
            ordered_dict["dish"] = item["dish"]
            ordered_dict["dish_cnt"] = item["dish_cnt"]
            ordered_dict["rank_by_frq"] = item["rank_by_cnt"]
            ordered_dict["rank_by_avg"] = item["rank_by_avg"]
            ordered_dict["avg_cos"] = item["avg_cos"]
            ordered_dict_list.append(ordered_dict)
        dic["rank"] = ordered_dict_list

        f_test.write(json.dumps(dic, indent=4))
        #sys.exit("stop")

        # 1/2 added by Tom. frequency rank of dishes.
        dish_list = sorted(dish_list, key=lambda k: k['dish_cnt'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_cnt"] = i+1

        rank_by_cnt = dish_list

        # ordered_dict -> solve the indention problem
        dic = {}
        dic["kendalltau_avg_frq"] = tau
        ordered_dict_list = []
        for item in dish_list:
            ordered_dict = OrderedDict()
            ordered_dict["dish"] = item["dish"]
            ordered_dict["dish_cnt"] = item["dish_cnt"]
            ordered_dict["rank_by_frq"] = item["rank_by_cnt"]
            ordered_dict["rank_by_avg"] = item["rank_by_avg"]
            ordered_dict["rank_by_max"] = item["rank_by_max"]
            ordered_dict["avg_cos"] = item["avg_cos"]
            ordered_dict["max_cos_10"] = item["max_cos_10"]
            ordered_dict["max_words"] = item["max_words"]
            ordered_dict_list.append(ordered_dict)
        dic["rank"] = ordered_dict_list

        return dic

    def render(self, dish_list):
        f = open("data/rank/restaurant_%s_rank.json"%self.rest_num,"w+")
        f.write(json.dumps(dish_list ,indent = 4))
        f.close()


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
    dishScore = DishScore()
    dish_list = dishScore.calculate()
    rank_by_avg = dishScore.rank(dish_list)
    dishScore.render(rank_by_avg)
