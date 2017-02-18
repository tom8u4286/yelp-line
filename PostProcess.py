import json
import uuid
from collections import OrderedDict
import sys
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

f_lexicon = open("data/lexicon/stanfer/stemmed_postive.txt")
lexicon_list = json.load(f_lexicon)
lexicon_list = ["-".join(line.split(" ")[:-1])+"_senti" for line in lexicon_list]

#Rendering the frontend_sentiment_statistics.json
for r in range(1,524):
    try:
        f_voc = open("data/voc/restaurant_%s_voc.txt"%r)
    except:
        print "cannot open file restaurant_%s_voc.txt"%r
        continue
    voc_list = [line.split(" ") for line in f_voc]
    tmp =[]
    for w in voc_list:
        first = int(w[0])
        tmp.append([int(w[0]),w[1].strip("\n")])
    voc_list = tmp

    f_dim2 = open("data/vectors/2dim/restaurant_%s_vector2_type3.json"%r)
    dim2_list = json.load(f_dim2)
    word_list = []
    index = 1

    for word in voc_list:
        if "_senti" in word[1]:
            for voc in dim2_list:
                if voc["word"] == word[1]:
                    tmp_dic = OrderedDict()
                    tmp_dic["index"] = index
                    tmp_dic["count"] = word[0]
                    tmp_dic["word"] = word[1]
                    tmp_dic["x"] = voc["vector2"][0]
                    tmp_dic["y"] = voc["vector2"][1]
                    index+=1
                    word_list.append(NoIndent(tmp_dic))
                    break
    f_output = open("data/frontend_sentiment/frontend_sentiment_rest%s.json"%r,"w+")
    f_output.write(json.dumps(word_list, indent=4, cls=NoIndentEncoder))

#Rendering the frontend_restaurant_dict_list.json

dict_list = []
rest_cnt = 1
for rest_num in range(1,524):
    try:
        rest_rank = json.load( open("data/rank/restaurant_%s_rank_type3.json"%rest_num))
    except:
        print "cannot open file /rank/restaurant_%s_rank_type3.json"%rest_num
        rest_cnt+=1
    try:
        rest_dict = json.load( open("data/restaurant_dict_list/restaurant_dict_%s.json"%rest_num))
    except:
        print "cannot open file /restaurant_dict_list/restaurant_dict_%s.json"%rest_num
        rest_cnt+=1
    try:
        rest_2dim = json.load( open("data/vectors/2dim/restaurant_%s_vector2_type3.json"%rest_num))
    except:
        print "cannot open file /vectors/2dim/restaurant_%s_vector2_type3.json"%rest_num
        rest_cnt+=1
        continue

    frq_list = []
    for i in range(1,6):
        for dish in rest_rank["rank"]:
            if dish["rank_by_frq"] == i:
                dish_name = ""
                for d in rest_dict["menu"]:
                    if dish["dish"] == d["name_ar"]:
                        dish_name = d["name"]
                        break
                dic = OrderedDict()
                dic["index"] = i
                dic["name"] = dish_name
                dic["name_ar"] = dish["dish"]
                dic["count"] = dish["dish_cnt"]
                dic["cosine_avg_score"] = dish["sum_higher0_cos"]
                dic["cosine_max_score"] = dish["max_cos_10"][0]
                dic["cosine_nearest"] = NoIndent([{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                dic["euclidean_avg_score"] = dish["sum_higher0_cos"]
                dic["euclidean_min_score"] = dish["max_cos_10"][0]
                dic["euclidean_nearest"] = NoIndent([{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                for w in rest_2dim:
                    if w["word"] == dish["dish"]:
                        dic["x"] = w["vector2"][0]
                        dic["y"] = w["vector2"][1]
                        break
                frq_list.append(dic)
                break

    cos_list = []
    for i in range(1,6):
        for dish in rest_rank["rank"]:
            if dish["rank_by_sum_higher_cos"]["0"] == i:
                dish_name = ""
                for d in rest_dict["menu"]:
                    if dish["dish"] == d["name_ar"]:
                        dish_name = d["name"]
                        break
                dic = OrderedDict()
                dic["index"] = i
                dic["name"] = dish_name
                dic["name_ar"] = dish["dish"]
                dic["count"] = dish["dish_cnt"]
                dic["cosine_avg_score"] = dish["sum_higher0_cos"]
                dic["cosine_max_score"] = dish["max_cos_10"][0]
                dic["cosine_nearest"] = NoIndent( [{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                dic["euclidean_avg_score"] = dish["sum_higher0_cos"]
                dic["euclidean_min_score"] = dish["max_cos_10"][0]
                dic["euclidean_nearest"] = NoIndent( [{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                for w in rest_2dim:
                    if w["word"] == dish["dish"]:
                        dic["x"] = w["vector2"][0]
                        dic["y"] = w["vector2"][1]
                        break
                cos_list.append(dic)
                break

    cos_max_list = []
    for i in range(1,6):
        for dish in rest_rank["rank"]:
            if dish["rank_by_max"] == i:
                dish_name = ""
                for d in rest_dict["menu"]:
                    if dish["dish"] == d["name_ar"]:
                        dish_name = d["name"]
                        break
                dic = OrderedDict()
                dic["index"] = i
                dic["name"] = dish_name
                dic["name_ar"] = dish["dish"]
                dic["count"] = dish["dish_cnt"]
                dic["cosine_avg_score"] = dish["sum_higher0_cos"]
                dic["cosine_max_score"] = dish["max_cos_10"][0]
                dic["cosine_nearest"] = NoIndent( [{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                dic["euclidean_avg_score"] = dish["sum_higher0_cos"]
                dic["euclidean_min_score"] = dish["max_cos_10"][0]
                dic["euclidean_nearest"] = NoIndent( [{"word":word,"cosine_similarity":cos} for cos, word in zip(dish["max_cos_10"],dish["max_words"])])
                for w in rest_2dim:
                    if w["word"] == dish["dish"]:
                        dic["x"] = w["vector2"][0]
                        dic["y"] = w["vector2"][1]
                        break
                cos_max_list.append(dic)
                break

    rest_dic = OrderedDict()
    rest_dic["index"] = rest_cnt
    rest_dic["restaurant_name"] = rest_dict["restaurant_name"]
    rest_dic["restaurant_id"] = rest_dict["restaurant_id"]
    rest_dic["stars"] = rest_dict["stars"]
    rest_dic["review_count"] = rest_dict["review_count"]
    rest_dic["top5_frequent"] = frq_list
    rest_dic["top5_cosine_avg"] = cos_list
    rest_dic["top5_cosine_max"] = cos_max_list
    rest_dic["top5_euclidean_avg"] = cos_list
    rest_dic["top5_euclidean_min"] = cos_max_list
    dict_list.append(rest_dic)
    rest_cnt+=1

f_dict_list = open("data/frontend_restaurant_dict_list.json","w+")
f_dict_list.write(json.dumps(dict_list, indent=4, cls=NoIndentEncoder))