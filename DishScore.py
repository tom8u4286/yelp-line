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
        self.build_type = int(re.search("type([0-9]+)", sys.argv[1].split("/")[3]).group(1))
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
        #print "rest name:",rest_name
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
            cos_list = [cos_matrix[dish_index][senti_index] for senti_index in senti_indices]
            avg_cos = sum(cos_list)/len(senti_indices)
            higher0_cos = sum( [num for num in cos_list if num > 0.0 ] )
            higher02_cos = sum( [num for num in cos_list if num > 0.2 ] )
            higher04_cos = sum( [num for num in cos_list if num > 0.4 ] )
            higher06_cos = sum( [num for num in cos_list if num > 0.6 ] )
            higher08_cos = sum( [num for num in cos_list if num > 0.8 ] )
            max_cos_10 = sorted( [cos_matrix[dish_index][senti_index] for senti_index in senti_indices], reverse=True )[:10]
            max_words = [words[ list(cos_matrix[dish_index]).index(max_cos) ] for max_cos in max_cos_10]

            dic["dish"] = words[dish_index]
            dic["avg_cos"] = avg_cos
            dic["sum_higher0_cos"] = higher0_cos
            dic["sum_higher02_cos"] = higher02_cos
            dic["sum_higher04_cos"] = higher04_cos
            dic["sum_higher06_cos"] = higher06_cos
            dic["sum_higher08_cos"] = higher08_cos
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

        #rank by max_cos_10
        dish_list = sorted(dish_list, key=lambda k: k['max_cos_10'][:1], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_max"] = i+1

        #rank by avg_cos
        dish_list = sorted(dish_list, key=lambda k: k['avg_cos'], reverse=True)
        for i in range( 0, len(dish_list)):
            dish_list[i]["rank_by_avg"] = i+1

        #rank by sum_higher0_cos of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['sum_higher0_cos'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_sum_higher0_cos"] = i+1

        #rank by sum_higher02_cos of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['sum_higher02_cos'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_sum_higher02_cos"] = i+1

        #rank by sum_higher04_cos of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['sum_higher04_cos'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_sum_higher04_cos"] = i+1

        #rank by sum_higher06_cos of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['sum_higher06_cos'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_sum_higher06_cos"] = i+1

        #rank by sum_higher08_cos of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['sum_higher08_cos'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_sum_higher08_cos"] = i+1

        #rank by frequency of dishes. 1/16 Added by Tom
        dish_list = sorted(dish_list, key=lambda k: k['dish_cnt'], reverse=True)
        for i in range(0, len(dish_list)):
            dish_list[i]["rank_by_cnt"] = i+1

        p_at10_avg, p_at20_avg, p_at30_avg = self.precision(dish_list,"rank_by_avg")
        p_at10_0, p_at20_0, p_at30_0 = self.precision(dish_list,"rank_by_sum_higher0_cos")
        p_at10_02, p_at20_02, p_at30_02 = self.precision(dish_list,"rank_by_sum_higher02_cos")
        p_at10_04, p_at20_04, p_at30_04 = self.precision(dish_list,"rank_by_sum_higher04_cos")
        p_at10_06, p_at20_06, p_at30_06 = self.precision(dish_list,"rank_by_sum_higher06_cos")
        p_at10_08, p_at20_08, p_at30_08 = self.precision(dish_list,"rank_by_sum_higher08_cos")
        p_at10_max, p_at20_max, p_at30_max = self.precision(dish_list,"rank_by_max")
        #print "p_at10: %s p_at20: %s p_at30: %s "%(p_at10, p_at20, p_at30)
        #sys.exit("stop")

        # ordered_dict -> solve the indention problem
        dic = OrderedDict()
        #dic["kendalltau_avg_frq"] = tau
        ordered_dict_list = []
        for item in dish_list:
            ordered_dict = OrderedDict()
            ordered_dict["dish"] = item["dish"]
            ordered_dict["dish_cnt"] = item["dish_cnt"]
            ordered_dict["rank_by_frq"] = item["rank_by_cnt"]
            ordered_dict["rank_by_sum_higher_cos"] = "0.0:%s, 0.2:%s, 0.4:%s, 0.6:%s, 0.8:%s"%(item["rank_by_sum_higher0_cos"],item["rank_by_sum_higher02_cos"],item["rank_by_sum_higher04_cos"],item["rank_by_sum_higher06_cos"],item["rank_by_sum_higher08_cos"])
            ordered_dict["rank_by_avg"] = item["rank_by_avg"]
            ordered_dict["rank_by_max"] = item["rank_by_max"]
            ordered_dict["avg_cos"] = item["avg_cos"]
            ordered_dict["max_cos_10"] = NoIndent(item["max_cos_10"])
            ordered_dict["max_words"] = NoIndent(item["max_words"])
            ordered_dict_list.append(ordered_dict)
        dic["precision_avg"] = "at10:%s, at20:%s, at30:%s"%(p_at10_avg, p_at20_avg, p_at30_avg)
        dic["precision_higher0"] = {"at10":p_at10_0, "at20":p_at20_0, "at30":p_at30_0 }
        dic["precision_higher02"] = {"at10":p_at10_02, "at20":p_at20_02, "at30":p_at30_02 }
        dic["precision_higher04"] = {"at10":p_at10_04, "at20":p_at20_04, "at30":p_at30_04 }
        dic["precision_higher06"] = {"at10":p_at10_06, "at20":p_at20_06, "at30":p_at30_06 }
        dic["precision_higher08"] = {"at10":p_at10_08, "at20":p_at20_08, "at30":p_at30_08 }
        dic["rank"] = ordered_dict_list
        return dic

    def precision(self, dish_list, method):
        num = 0.0
        for dish in dish_list:
            if dish["rank_by_cnt"] <= 10 and dish[method] <= 10:
                num +=1.0
        p_at10 = num / 10.0

        num = 0.0
        for dish in dish_list:
            if dish["rank_by_cnt"] <= 20 and dish[method] <= 20:
                num +=1.0
        p_at20 = num / 20.0

        num = 0.0
        for dish in dish_list:
            if dish["rank_by_cnt"] <= 30 and dish[method] <= 30:
                num +=1.0
        p_at30 = num / 30.0

        return p_at10, p_at20, p_at30

    def render(self, dish_list):


        f = open("data/rank/restaurant_%s_rank_type%s.json"%(self.rest_num, self.build_type),"w+")
        f.write(json.dumps(dish_list ,indent = 4, cls=NoIndentEncoder))
        f.close()
        print "DishScore.py rest_%s_type%s completed"%(self.rest_num, self.build_type)


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
