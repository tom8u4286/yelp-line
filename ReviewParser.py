# -*- coding: utf-8 -*-
import sys, re, json, os, uuid, itertools
from operator import itemgetter
from collections import OrderedDict
#import SpellingChecker #self defined
import unicodedata
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class ReviewParser:
    """ This program aims to transform restaurant_*.json into
        (1) restaurant_*.txt in 'data/backend_reviews'
        (2) restaurant_dict_*.json in 'data/restaurant_dic_list'
        (3) restaurant_1.json in 'data/frontend_reviews'
        (4) count sentiment words in the reviews
    """

    def __init__(self):
        print "Processing", sys.argv[1]
        self.src = sys.argv[1]  # E.g. data/reviews/restaurant_3.json
        self.src_b = 'data/business_list.json'

        self.backend_reviews = []
        self.frontend_reviews = []
        self.clean_reviews = []

        self.filename = ""
        self.restaurant_name = ""

        self.senti_matched_cnt = 0

        self.switch = 1

    def get_review_dict(self):
        with open(self.src) as f:
            review_dic = json.load(f)

        return review_dic

    def get_business(self):
        """ match business_id in review_dict with business_list.json """
        review_dic = self.get_review_dict()
        with open(self.src_b) as f:
            business_list = json.load(f)

        for business in business_list:
            if business["business_id"] == review_dic["business_id"]:
                matched_business = business

        return matched_business

    def get_lexicon(self):
        """ return p_list containing dictionaries of positive words """
        """ 12/17/2016 Tom change the lexicon to stanfer lexicon. positive"""

        with open('data/lexicon/stanfer/positive.txt') as f:
            pos_list = [word.strip("\n") for word in f]

        return pos_list

    def get_clean_menu(self):
        """ get menu from business_list and return a clean menu"""
        menu = self.get_business()["menu"]
        clean_menu = []

        for dish in menu:
            dish = re.sub("\(.*\)", "", dish)
            dish = dish.replace("(","").replace(")","")
            dish = dish.replace("&", "and").replace("\'", "").replace("*","").replace("-"," ")
            dish = re.sub("(\s)+", " ", dish)
            dish = dish.strip()
            dish = re.sub("(!|@|#|\$|%|\^|\*\:|\;|\.|\,|\"|\'|\\|\/)", r'', dish)

            clean_menu.append(dish)

        #print clean_menu
        return clean_menu

    def get_dishes_regex(self):
        """ dishes_regex is the regular expression for every dish in the dish_list # about to be changed """
        dishes_regex = self.get_clean_menu()

        for i in xrange(len(dishes_regex)):

            dishes_regex[i] = dishes_regex[i].lower()
            dishes_regex[i] = dishes_regex[i].split()
            dishes_regex[i][0]= "(" + dishes_regex[i][0] # adding '(' before the first word

            for word in xrange(len(dishes_regex[i])-1):
                dishes_regex[i][word] += "\\s*"

            for word in xrange(len(dishes_regex[i])-2):
                dishes_regex[i][word] += "|"

            dishes_regex[i][len(dishes_regex[i])-2] = dishes_regex[i][len(dishes_regex[i])-2] + ")+"
            dishes_regex[i] = "".join(dishes_regex[i])[:-1]
            dishes_regex[i] += "[a-z]+(s|es|ies)?"

        return dishes_regex

    def get_dishes_ar(self):
        """ dishes_ar is the dish_list with every dish 'a'ppending 'r'estaurant_name E.g. dish_restaurant """
        dishes_ar = self.get_clean_menu()
        restaurant_name = self.get_business()['business_name']
        self.restaurant_name = restaurant_name

        for i in xrange(len(dishes_ar)):
            dishes_ar[i] = dishes_ar[i].replace(" ", "-") + "_" + restaurant_name.replace(" ", "-")
            dishes_ar[i] = re.sub("(\s)+", r" ", dishes_ar[i])
            dishes_ar[i] = dishes_ar[i].lower().replace("&", "and").replace("\'", "").replace(".", "").replace(",","")

        return dishes_ar

    def get_marked_dishes(self):
        """ match the dishes in the reviews and mark the dish"""
        menu = self.get_clean_menu()
        marked_dishes = []

        if self.switch:
            print "\n" + "-"*70
            print "Marking dishes"

        cnt = 0
        length = len(menu)
        for dish in menu:
            cnt += 1
            dish = dish.lower().replace("&","and").replace("'","").replace(" ","-")
            marked_dishes.append(" <mark>" + dish + "</mark> ")

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
                sys.stdout.flush()

        return marked_dishes

    def get_clean_reviews(self):
        """ clean reviews """
        raw_reviews = self.get_review_dict()["reviews"]

        if self.switch:
            print "\nCleaning reviews"

        cnt = 0
        length = len(raw_reviews)
        clean_reviews = []
        for text in raw_reviews:
            cnt += 1

            text = re.sub(r'https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)
            text = text.replace("!","").replace("@","").replace("#","").replace("$","").replace("%","")
            text = text.replace("^","").replace("&","").replace("*","").replace("(","").replace(")","")
            text = text.replace(":","").replace(";","").replace(".","").replace(",","").replace("=", "")
            text = text.replace("+","").replace("-","").replace("|","").replace("\\","").replace("/","")
            text = text.replace("~","").replace("_", "").replace(">","").replace("<", "").replace("?", "")
            text = text.replace("\""," ").replace("[","").replace("]","").replace("{","").replace("}","")

            text = re.sub(r"'m", " am", text)
            text = re.sub(r"'re", " are", text)
            text = re.sub(r"'s", " is", text)
            text = re.sub(r"'ve", " have", text)
            text = re.sub(r"'d", " would", text)
            text = re.sub(r"n't", " not", text)
            text = re.sub(r"'ll", " will", text)

            text = text.replace("\'"," ")

            #FIXME Remove accents
            text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

            #FIXME porterStemmer # but may lose information

            text = re.sub("(\\n)+", r" ", text)
            text = re.sub("(\s)+", r" ", text)

            text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text)) # sooo happppppy -> so happy
            clean_reviews.append(text)

            sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
            sys.stdout.flush()

        print "clean_reviews complete...length of clean ", len(clean_reviews)
        return clean_reviews

    def get_frontend_review_dict_list(self):

        frontend_reviews = list(self.clean_reviews)
        dishes = self.get_clean_menu()
        dishes_regex = self.get_dishes_regex()
        marked_dishes = self.get_marked_dishes()

        if self.switch:
            print "\n" + "-"*70
            print "Processing frontend reviews"

        frontend_review_dict_list = []
        length1 = len(marked_dishes)
        for i in xrange(len(marked_dishes)):
            length2 = len(frontend_reviews)
            for j in xrange(len(frontend_reviews)):
                frontend_reviews[j] = frontend_reviews[j]
                frontend_reviews[j] = re.sub("\\n+", r" ", frontend_reviews[j])

                """ Replacing | E.g. I love country pate. -> I love <mark>housemade country pate</mark>. """
                frontend_reviews[j] = re.sub(dishes_regex[i], marked_dishes[i], frontend_reviews[j], flags = re.IGNORECASE)

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s"%(i+1, length1, j+1, length2))
                    sys.stdout.flush()

            reviews = []
            for k in xrange(len(frontend_reviews)):
                if marked_dishes[i] in frontend_reviews[k]:
                    frontend_reviews[k] = frontend_reviews[k].replace("-"," ")

                    frontend_reviews[k] = frontend_reviews[k].replace(" ! ","! ").replace(" @ ","@ ").replace(" # ","# ").replace(" $ ","$ ").replace(" % ","% ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" ^ ","^ ").replace(" & ","& ").replace(" * ","* ").replace(" ( ","( ").replace(" ) ",") ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" : ",": ").replace(" ; ","; ").replace(" . ",". ").replace(" , ",", ").replace(" = ", "= ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" + ","+ ").replace(" - ","- ").replace(" | ","| ")
                    frontend_reviews[k] = frontend_reviews[k].replace(" ~ ","~ ").replace(" > ","> ").replace(" < ", "< ").replace(" ? ", "? ")
                    frontend_reviews[k] = re.sub("(\s)+", r" ", frontend_reviews[k])

                    reviews.append(frontend_reviews[k])

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s"%(i+1, length1, k+1, length2))
                    sys.stdout.flush()

            frontend_review_dict_list.append({"dish_name": dishes[i], "reviews": reviews})

        return frontend_review_dict_list

    def add_senti(self,backend_reviews):
        """2016/12/17 Tom added the function.(the sentiment would be stemmed.)"""
        print "\nAdding _senti after stemmed sentiment words.... "
        stemmer = SnowballStemmer('english')
        pos_list = self.get_lexicon()
        words_length = len(pos_list)
        review_list = backend_reviews
        review_list_length = len(backend_reviews)
        matched_cnt = 0
        review_cnt = 0
        new_reviews_list = []
        for review in review_list:
            review_cnt += 1
            new_review = " "+review+" "
            word_cnt = 0
            for word in pos_list:
                word_cnt += 1
                if "-" or "_" in word:
                    word = word.replace("-","=")
                    word = word.replace("_","=")
                    word = word.split("=")
                    word = [stemmer.stem(w) for w in word]
                    word = " ".join(word)
                else:
                    word = stemmer.stem(w)

                word_senti = word.replace(" ","-")+"_senti"
                if word+" " in review:
                    new_review = new_review.replace(" "+word+" ", " "+word_senti+" ",5)
                    matched_cnt += 1
                sys.stdout.write("\rtotally matched: %s, reviews: %s / %s, senti_words: %s / %s  "%(matched_cnt, review_cnt, review_list_length, word_cnt, words_length))
                sys.stdout.flush()
            new_reviews_list.append(new_review.strip())
        self.senti_matched_cnt = matched_cnt
        return new_reviews_list

    def stem(self, backend_reviews):
        """2016/12/17 Tom added the function."""
        #stop_words = set(stopwords.words('english'))
        stemmer = SnowballStemmer('english')
        length = len(backend_reviews)
        print "\nStemming backend reviews...."
        new_reviews_list = []
        review_cnt = 0
        for review in backend_reviews:
            review_cnt += 1
            word_tokens = review.split(" ")
            #"""remove stop words"""
            #filtered_sentence = [w for w in word_tokens if not w in stop_words]
            """stemming"""
            filtered_sentence = [stemmer.stem(w) for w in word_tokens]
            """join back the review from a list to a string"""
            new_review = " ".join(filtered_sentence)
            new_reviews_list.append(new_review)
            sys.stdout.write("\rreviews: %s / %s"%(review_cnt, length))
            sys.stdout.flush()

        return new_reviews_list

    def remove_stopwords(self, backend_reviews):
        """2016/12/22 Tom added the function."""
        stop_words = set(stopwords.words('english'))
        length = len(backend_reviews)
        print "\nRemoving stopwords..."
        new_reviews_list = []
        review_cnt = 0
        for review in backend_reviews:
            review_cnt += 1
            word_tokens = review.split(" ")
            """remove stop words"""
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            """join back the review from a list to a string"""
            new_review = " ".join(filtered_sentence)
            new_reviews_list.append(new_review)
            sys.stdout.write("\rreviews: %s / %s    "%(review_cnt, length))
            sys.stdout.flush()

        return new_reviews_list

    def get_backend_reviews(self):
        """ match the dishes in the reviews with dishes_regex and replace them with the dishes in dishes_ar  """
        """2016/12/17 Tom added the '_senti' after sentiment words , stopwords and stemmer. """
        backend_reviews = list(self.clean_reviews)
        print "\nlength of self.clean_reviews: ", len(backend_reviews)
        dishes_regex = self.get_dishes_regex()
        dishes_ar = self.get_dishes_ar()

        if self.switch:
            print "\n" + "-"*70
            print "Processing backend_reviews"

        length1 = len(backend_reviews)
        for i in xrange(len(backend_reviews)):
            length2 = len(dishes_regex)
            for j in xrange(len(dishes_regex)):
                backend_reviews[i] = backend_reviews[i].lower()
                """ Replacement | E.g. I love country pate. -> I love housemade-country-pate_mon-ami-gabi. """
                backend_reviews[i] = re.sub(dishes_regex[j], dishes_ar[j], backend_reviews[i], flags = re.IGNORECASE)
                backend_reviews[i] = re.sub("(\s)+", r" ", backend_reviews[i])

                if self.switch:
                    sys.stdout.write("\rStatus: %s / %s | %s / %s    "%(i+1, length1, j+1, length2))
                    sys.stdout.flush()

        backend_reviews = self.stem(backend_reviews)
        print "\nlength of self.backend_reviews stemmed: ", len(backend_reviews)
        backend_reviews = self.add_senti(backend_reviews)
        print "\nlength of backend_reviews add_senti: ", len(backend_reviews)
        backend_reviews = self.remove_stopwords(backend_reviews)
        print "\nlength of backend_reviews remove_stopwords: ",len(backend_reviews)

        print "get_backend_reviews complete... the length of backend_review:", len(backend_reviews)
        return backend_reviews

    def get_restaurant_dict(self):
        """ match backend_review_list with dish_ar count the frequnecy of every dish"""

        business = self.get_business()
        #backend_reviews = self.get_backend_reviews()
        dishes_ar = self.get_dishes_ar()

        if self.switch:
            print "\n" + "-"*70
            print "Processing restaurant_dict"

        count_list = []
        count = 0
        """ counting the frequencies of dish in reviews"""
        cnt = 0
        length = len(dishes_ar)
        for dish in dishes_ar:
            cnt += 1
            for review in self.backend_reviews:
                print dish
                count += review.count(dish)
                if dish == u"alcoholiemergen-c-drink_mon-ami-gabi":
                    print count
                    sys.exit("stop")
            count_list.append(count)
            count = 0

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(cnt, length))
                sys.stdout.flush()

        """counting the avg_word per review."""
        review_avg_words = sum([len(review.split(" ")) for review in self.backend_reviews])/len(self.backend_reviews)
        business["avg_words_per_review"] = review_avg_words

        """counting the average lenght of sentiment words and dish words."""
        business["dish_senti_avg_lenght"] = self.count_senti_lenght()

        menu = self.get_clean_menu()
        """ sorted by count """
        i = 0
        dish_dict_list = []
        for i in xrange(len(menu)):
            dish_dict = {"count": count_list[i], "name": menu[i], "name_ar": dishes_ar[i]}
            i += 1
            dish_dict_list.append(dish_dict)
        dish_dict_list = sorted(dish_dict_list, key=itemgetter('count'), reverse = True)

        index = 0
        processed_menu = []
        for dish_dict in dish_dict_list:
            index += 1
            orderedDict = OrderedDict()
            orderedDict["index"] = index
            orderedDict["count"] = dish_dict["count"]
            orderedDict["name"] = dish_dict["name"]
            orderedDict["name_ar"] = dish_dict["name_ar"]
            orderedDict["x"] = 0
            orderedDict["y"] = 0

            processed_menu.append(NoIndent(orderedDict))

        business["menu"] = processed_menu
        restaurant_dict = business

        return restaurant_dict

    def get_statistics(self):
        """ count the sentiment word in reviews """
        #backend_reviews = self.get_backend_reviews()
        positive_list = self.get_lexicon()

        if self.switch:
            print "\n" + "-"*70
            print "Processing statistics"

        statistics = []
        index_cnt = 0
        length = len(positive_list)

        for word in positive_list:
            index_cnt += 1
            dish_count = 0
            for review in self.backend_reviews:
                dish_count += review.count(" " + word + " ")
            orderedDict = OrderedDict()
            orderedDict["index"] = index_cnt
            orderedDict["word"] = word
            orderedDict["count"] = dish_count
            statistics.append(NoIndent(orderedDict))

            if self.switch:
                sys.stdout.write("\rStatus: %s / %s"%(index_cnt, length))
                sys.stdout.flush()

        return statistics

    def create_dirs(self):
        """ create the directory if not exist"""
        dir1 = os.path.dirname("data/backend_reviews/")
        dir2 = os.path.dirname("data/frontend_reviews/")
        dir3 = os.path.dirname("data/restaurant_dict_list/")
        dir4 = os.path.dirname("data/sentiment_statistics/")

        if not os.path.exists(dir1):
            os.makedirs(dir1)
        if not os.path.exists(dir2):
            os.makedirs(dir2)
        if not os.path.exists(dir3):
            os.makedirs(dir3)
        if not os.path.exists(dir4):
            os.makedirs(dir4)

    def render_frontend_reviews(self):

        total_review_count = len(self.clean_reviews)
        """ (1) render restaurant_*.json in ./frontend_reviews """

        orderedDict1 = OrderedDict()
        orderedDict1["restaurant_name"] = business["business_name"]
        orderedDict1["restaurant_id"] = business["business_id"]
        orderedDict1["stars"] = business["stars"]
        orderedDict1["total_review_count"] = total_review_count

        ordered_frontend_review_dict_list = []
        dish_cnt = 0
        for review_dict in self.frontend_review_dict_list:
            dish_cnt += 1
            tmp_ordered_dict = OrderedDict()
            tmp_ordered_dict['dish_index'] = dish_cnt
            tmp_ordered_dict['dish_name'] = review_dict["dish_name"]
            tmp_ordered_dict['reviews'] = review_dict["reviews"]
            ordered_frontend_review_dict_list.append(tmp_ordered_dict)

        orderedDict1["dish_reviews"] = ordered_frontend_review_dict_list

        frontend_json = open("data/frontend_reviews/restaurant_%s.json"%(self.filename), "w+")
        frontend_json.write(json.dumps( orderedDict1, indent = 4))
        frontend_json.close()

        print sys.argv[1], "'s frontend json is completed"

    def render_backend_reviews(self):
        """ (2) render restaurant_*.txt in ./backend_reviews """
        backend_txt = open("data/backend_reviews/restaurant_%s.txt"%(self.filename), "w+")
        for review in self.backend_reviews:
            backend_txt.write(review.encode("utf-8") + '\n')
        backend_txt.close()

        print sys.argv[1], "'s backend txt is completed"

    def render_restaurant_dict(self, restaurant_dict):

        total_review_count = len(self.backend_reviews)
        """ (3) render restaurant_dict, in which menu is transformded from a list to a detailed dictionary """

        orderedDict2 = OrderedDict()
        orderedDict2["restaurant_name"] = restaurant_dict["business_name"]
        orderedDict2["restaurant_id"] = restaurant_dict["business_id"]
        orderedDict2["stars"] = restaurant_dict["stars"]
        orderedDict2["review_count"] = total_review_count
        orderedDict2["avg_word_count_pre_review"] = restaurant_dict["avg_words_per_review"]
        orderedDict2["menu_length"] = restaurant_dict["menu_length"]
        orderedDict2["senti_per_review"] = float(self.senti_matched_cnt) / float(total_review_count)
        orderedDict2["dish_senti_avg_len"] = restaurant_dict["dish_senti_avg_lenght"]
        orderedDict2["menu"] = restaurant_dict["menu"]

        #dish_list = sorted(dish_list, key=lambda k: k['count'])

        restaurant_json = open("data/restaurant_dict_list/restaurant_dict_%s.json"%(self.filename), "w+")
        restaurant_json.write(json.dumps( orderedDict2, indent = 4, cls=NoIndentEncoder))
        restaurant_json.close()

        print sys.argv[1], "'s restaurant_dic json is completed"

    def render_sentiment_statistics(self):
        """ (4) render restaurant.json containing dictionaries of each positive sentiment word """

        restaurant_json = open("data/sentiment_statistics/restaurant_%s.json"%(self.filename), "w+")
        restaurant_json.write(json.dumps(sentiment_statistics, indent = 4, cls=NoIndentEncoder))
        restaurant_json.close()

        print sys.argv[1], "'s sentiment analysis is completed"

    def render_compare_file(self):
        """ (5) render compare json file."""
        """12/23 Tom added."""
        compare_file = open("data/backend_reviews/restaurant_%s_comapre.json"%(self.filename),"w+")
        lst = []
        for idx, review in enumerate(self.clean_reviews):
            orderedDict3 = OrderedDict()
            orderedDict3["origin"] = review
            orderedDict3["new"] = self.backend_reviews[idx]
            lst.append(orderedDict3)
        compare_file.write(json.dumps(lst, indent = 4))
        print sys.argv[1], "'s compare file is completed."

    def count_senti_lenght(self):
        """12/29 Tom added."""

        length_list = []
        err_cnt = 0
        tmp_list = []
        for review in self.backend_reviews:

            if "_senti" in review:
                review = review.split(" ")
                dish_idx = []
                restaurant_name = self.restaurant_name.lower().replace(" ","-")
                for idx, word in enumerate(review):
                    if restaurant_name in word:
                        dish_idx.append(idx)

                if len(dish_idx) > 0:
                    for idx in dish_idx:
                        cnt = 1
                        while True:
                            if idx+cnt < len(review):
                                if "_senti" in review[idx+cnt]:
                                    length_list.append(cnt)
                                    break
                            elif idx-cnt > 0:
                                if "_senti" in review[idx-cnt]:
                                    length_list.append(cnt)
                                    break
                            elif idx+cnt > len(review) and idx-cnt < 0:
                                break
                            cnt+=1
        avg_length = float(sum(length_list))/float(len(length_list))

        return avg_length

    def render(self):
        """ render frontend_review & backend_reviews & restaurant_list """
        business = self.get_business()
        self.menu = self.get_clean_menu()
        self.clean_reviews = self.get_clean_reviews()
        #self.frontend_review_dict_list = self.get_frontend_review_dict_list()
        self.backend_reviews = self.get_backend_reviews()

        restaurant_dict = self.get_restaurant_dict()
        sentiment_statistics = self.get_statistics()

        self.create_dirs()

        if self.switch:
            print "\n" + "-"*70
            print "Rendering"

        self.filename = sys.argv[1][24]
        if sys.argv[1][25] != ".":
            self.filename = self.filename + sys.argv[1][25]
            if sys.argv[1][26] != ".":
                self.filename = self.filename + sys.argv[1][26]

        #self.render_frontend_reviews()
        self.render_backend_reviews()
        self.render_restaurant_dict(restaurant_dict)
        #self.render_sentiment_statistics_reviews()
        self.render_compare_file()

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

if  __name__ == '__main__':
    parser = ReviewParser()
    parser.render()
