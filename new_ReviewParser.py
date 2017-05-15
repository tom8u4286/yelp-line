import sys, re, json, os, uuid
import unicodedata
from collections import OrderedDict
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from operator import itemgetter

class new_ReviewParser:
    """This program aims to transform raw_review restaurant_*.json into
    1. backend_reviews
    2. frontend_reviews
    3. restaurant_dict_*.json
    4. sentiment_statistic
    """
    def __init__(self):
        self.testing = False
        if self.testing == True:
            print "Start processing file restaurant_%s.json..."%(sys.argv[1])

        self.rest_num = sys.argv[1]
        self.rest_name, self.rest_id, self.raw_reviews = self.get_rest_info()
        self.raw_dishes, self.dishes_regex, self.dishes_ar, self.append_rest_name = self.get_dishes_info()
        self.lexicon = self.get_lexicon()
        self.backend_reviews = []
        self.backend_reivews_processed = False

    def get_rest_info(self):
        f = open("data/reviews/restaurant_%s_raw.json"%self.rest_num)
        dic = json.load(f)
        return dic["business_name"], dic["business_id"], dic["reviews"]

    def get_lexicon(self):
        f = open("data/lexicon/stanfer/positive.txt")
        pos_list = [word.strip("\n").replace("_"," ").replace("-"," ") for word in f]
        return pos_list

    def get_dishes_info(self):
        dic = json.load(open("data/new_business_list.json"))
        #get raw_dishes
        raw_dishes = []
        for rest in dic:
            if rest["business_id"]== self.rest_id:
                raw_dishes = rest["menu"]
                break
        raw_dishes = sorted(raw_dishes, key=len, reverse=True)

        #get dishes_regex
        cleaned_menu = []
        for dish in raw_dishes:
            dish = dish.lower().replace('_',' ').replace(' & ',' and ').replace(' or ', ' ').replace('\'s','')
            re_token = re.compile('[a-z][a-z]+')
            dish = ' '.join(re_token.findall(dish))
            if len(dish) > 2:
                cleaned_menu.append(dish)
        dishes_regex = []
        for dish in cleaned_menu:
            token_list = dish.split(' ')
            if len(token_list) == 1:
                regex = '\s(' + token_list[0][:-1] + ')[a-z]+(s|es|ies)?\s'
                dishes_regex.append(regex)
            elif len(token_list) > 1:
                for i in xrange(len(token_list)-1):
                    token_list[i] += '\s*'
                for i in xrange(len(token_list)-2):
                    token_list[i] += '|'
                regex = '\s(' + ''.join(token_list[:-1]) + ')+' + token_list[-1:][0][:-1] + '[a-z]+(s|es|ies)?\s'
                dishes_regex.append(regex)

        #get dishes_ar
        append_rest_name = re.sub('([^\w])+',' ', self.rest_name.strip('\'s')).lower().replace(' ', '-')
        dishes_ar = [ dish.replace(' ','-') + '_' + append_rest_name  for dish in cleaned_menu]

        return raw_dishes, dishes_regex, dishes_ar, append_rest_name

    def render_backend_reviews(self):
        #(1)remove punctuation and urls
        #'m --> am
        cnt = 0
        if self.testing == True:
            print "------------------------------------"
            print "Start processing backend review...."
            print '(1) Cleaning reviews...'
        cleaned_reviews = []
        comparing_reviews = []
        length = len(self.raw_reviews)
        for review in self.raw_reviews:
            review = review.lower().strip()
            review = re.sub(r'https?:\/\/.*[\r\n]*', ' ', review, flags=re.MULTILINE)
            review = review.replace('\'m',' am').replace('\'re',' are').replace('\'s',' is').replace('\'ve',' have')
            review = review.replace('\'d',' would').replace('n\'t', ' not').replace('\'ll',' will')
            review = review.replace('\n',' ')
            #remove accents
            review = unicodedata.normalize('NFKD', review).encode('ASCII', 'ignore')
            #comparing reviews contains punctuations
            comparing_reviews.append(review)

            #cleaned_reviews doesn't contains punctuations
            review = re.sub('([^\w])+',' ',review)
            cleaned_reviews.append(review)

            if self.testing == True:
                cnt += 1
                sys.stdout.write('\rStatus: %s / %s'%(cnt, length))
                sys.stdout.flush()

        #(2)add senti
        if self.testing == True:
            print '\n(2) Adding _senti...'
            cnt = 0
        senti_reviews = []
        for review in cleaned_reviews:
            for senti in self.lexicon:
                if senti+' ' in review+' ':
                    review = review.replace(senti+' ', senti.replace(' ','-')+'_senti ',5)
            senti_reviews.append(review)
            if self.testing == True:
                cnt+=1
                sys.stdout.write('\rStatus: %s / %s'%(cnt, length))
                sys.stdout.flush()

        #(3)remove stopwords
        if self.testing == True:
            print '\n(3) Removing stopwords...'
            cnt = 0
        stop_words = set(stopwords.words('english'))
        stop_removed_reviews = []
        for review in senti_reviews:
            word_tokens = review.split(' ')
            words_stop_removed = [w for w in word_tokens if w not in stop_words]
            stop_removed_reviews.append(' '.join(words_stop_removed))
            if self.testing == True:
                cnt += 1
                sys.stdout.write('\rStatus: %s / %s'%(cnt, length))
                sys.stdout.flush()

        #(4)repalce dishes
        if self.testing == True:
            print '\n(4) Replacing dishes into dish_ar...'
            cnt = 0
        dish_ar_review = []
        for review in stop_removed_reviews:
            #The reason of adding space in front and back of review is let regex match word by word
            review = ' ' + review + ' '
            for dish_regex, dish_ar in zip(self.dishes_regex, self.dishes_ar):
                #The reason of adding spaces in front and back of the dish_ar is beacuse we added \s in the regex
                review = re.sub(dish_regex, ' '+dish_ar+' ', review)
            dish_ar_review.append(review)
            if self.testing == True:
                cnt += 1
                sys.stdout.write('\rStatus: %s / %s'%(cnt, length))
                sys.stdout.flush()

        #(5)stemming backend reviews
        if self.testing == True:
            print '\n(5) Stemming backend reviews...'
            cnt = 0
        stemmer = SnowballStemmer('english')
        stemmed_reviews = []
        for review in dish_ar_review:
            review = review.split(' ')
            words_stemmed = [stemmer.stem(w) if '_' not in w else w for w in review]
            stemmed_reviews.append(' '.join(words_stemmed))
            if self.testing == True:
                cnt += 1
                sys.stdout.write('\rStatus: %s / %s'%(cnt, length))
                sys.stdout.flush()

        #(6)Rendering file
        f = open('data/backend_reviews/restaurant_%s.txt'%self.rest_num,'w+')
        #lst = []
        #for stop, stem in zip(stop_removed_reviews, stemmed_reviews):
        #    lst.append(stop)
        #    lst.append(stem)
        f.write('\n'.join(stemmed_reviews))

        self.backend_reviews = stemmed_reviews
        self.backend_reivews_processed = True
        if self.testing == True:
            print "\nrestaurant_%s.txt backend review rendered."%self.rest_num


        #(7)Rendering compare file
        f = open('data/compare/restaurant_%s.json'%self.rest_num,'w+')
        lst = []
        for origin, back in zip(comparing_reviews, self.backend_reviews):
            dic = {}
            dic['origin'] = origin
            dic['backend_review'] = back
            lst.append(dic)
        f.write(json.dumps(lst, indent = 4))

        if self.testing == True:
            print "\nrestaurant_%s.txt comparing review (before and after preprocessed) rendered."%self.rest_num

    def render_frontend_reviews(self):
        #(1)marking the dishes
        if self.testing == True:
            print "------------------------------------"
            print "Start rendering frontend review..."
            print 'Marking dishes <mark>...'
        dish_cnt = 1
        menu_length, review_length = len(self.raw_dishes), len(self.raw_reviews)

        markedReviewList = []
        review_cnt = 1
        for review in self.raw_reviews:
            review = review.lower()
            review = review.replace(' and ',' ').replace(' & ',' ').replace('\n',' ')
            review = review.replace('.',' . ').replace(',',' , ').replace('!',' ! ').replace('?',' ? ')
            review = review.replace('(',' ( ').replace(')',' ) ')

            dish_cnt =1
            for dish_regex, raw_dish in zip(self.dishes_regex, self.raw_dishes):
                review = re.sub(dish_regex,' <mark>'+raw_dish+'</mark> ', review)
                if self.testing == True:
                    sys.stdout.write('\rReviews: %s / %s  Dishes: %s / %s '%(review_cnt, review_length,dish_cnt, menu_length ))
                    sys.stdout.flush()
                    dish_cnt +=1
            review = re.sub('\s+',' ',review)
            markedReviewList.append(review)
            review_cnt +=1

        dishes_reviews = []
        dish_cnt = 1
        for raw_dish in self.raw_dishes:
            dish_reviews_list = [review for review in markedReviewList if '<mark>'+raw_dish+'</mark>' in review]
            dic = OrderedDict()
            dic['dish_index'] = dish_cnt
            dic['dish_name'] = raw_dish
            dic['reviews'] = dish_reviews_list
            dishes_reviews.append(dic)
            dish_cnt += 1

        #(2)rendering file
        frontend_dic = OrderedDict()
        frontend_dic['restaurant_name'] = self.rest_name
        frontend_dic['restaurant_id'] = self.rest_id
        frontend_dic['total_review_count'] = review_cnt
        frontend_dic['dish_reviews'] = dishes_reviews

        f = open('data/frontend_reviews/restaurant_%s.json'%(self.rest_num),'w+')
        f.write(json.dumps(frontend_dic, indent = 4))

        if self.testing == True:
            print "\nrestaurant_%s.json frontend review rendered."%self.rest_num


    def render_restaurant_dict(self):
        if self.testing == True:
            print "------------------------------------"
            print "Start rendering restaurant_dict..."
            print '(1) Counting reviews avg length...'
            cnt = 1
        #(1)Counting the reviews avg length and number of senti in a review
        word_counts = 0
        senti_counts = 0
        review_length = len(self.raw_reviews)
        for review in self.backend_reviews:
            senti_counts += review.count('_senti')
            word_counts += len(review.split(' '))
            if self.testing == True:
                sys.stdout.write('\rStatus: %s / %s'%(cnt, review_length))
                sys.stdout.flush()
                cnt+=1

        #(2)Counting the avg lenght between dish words and senti words
        if self.testing == True:
            print '\n(2) Counting avg length between dish words and senti words...'
            cnt = 1
        avg_length = []
        for review in self.backend_reviews:
            if self.append_rest_name in review and '_senti' in review:
                review = review.split(' ')
                senti_indices = [idx for idx, word in enumerate(review) if '_senti' in word]
                dish_indices = [idx for idx, word in enumerate(review) if self.append_rest_name in word]

                length_lst = []
                for idx_d in dish_indices:
                    length_lst.append(min([abs(idx_d-idx_s) for idx_s in senti_indices]))
                avg_length.append(float(sum(length_lst))/float(len(length_lst)))
            if self.testing == True:
                sys.stdout.write('\rStatus: %s / %s'%(cnt, review_length))
                sys.stdout.flush()
                cnt+=1

        #(3)Counting the dish words
        if self.testing == True:
            print '\n(3) Counting the number of dish words...'
        menu_length = len(self.dishes_ar)
        menu_lst = []
        dish_cnt = 1
        for raw_dish, dish_ar, dish_regex in zip(self.raw_dishes, self.dishes_ar, self.dishes_regex):
            dish_total = 0
            mentioned_review_num = 0
            review_cnt = 1
            for review in self.backend_reviews:
                dish_total += review.count(dish_ar)
                if dish_ar in review:
                    mentioned_review_num += 1
                if self.testing == True:
                    sys.stdout.write('\rDishes: %s / %s Reviews: %s / %s  '%(dish_cnt, menu_length, review_cnt, review_length))
                    sys.stdout.flush()
                    review_cnt += 1
            dic = {}
            dic['count'] = dish_total
            dic['mentioned_review_num'] = mentioned_review_num
            dic['name'] = raw_dish
            dic['name_ar'] = dish_ar
            dic['regex'] = dish_regex
            menu_lst.append(dic)
            dish_cnt+=1
        menu_lst = sorted(menu_lst, key=itemgetter('count'), reverse= True)
        menu = []
        for idx, dish in enumerate(menu_lst):
            dic = OrderedDict()
            dic['index'] = idx +1
            dic['count'] = dish['count']
            dic['mentioned_review_num'] = dish['mentioned_review_num']
            dic['name'] = dish['name']
            dic['name_ar'] = dish['name_ar']
            dic['regex'] = dish['regex']
            menu.append(NoIndent(dic))

        #(3)Rendering file
        rest_dic = OrderedDict()
        rest_dic['restaurant_name'] = self.rest_name
        rest_dic['restaurant_id'] = self.rest_id
        rest_dic['append_rest_name'] = self.append_rest_name
        rest_dic['review_count'] = review_length
        rest_dic['avg_word_count_pre_review'] = float(word_counts)/float(review_length)
        rest_dic['menu_length'] = menu_length
        rest_dic['senti_per_review'] = float(senti_counts)/float(review_length)
        rest_dic['dish_senti_avg_len'] = sum(avg_length)/float(len(avg_length))
        rest_dic['menu'] = menu
	f = open('data/restaurant_dict_list/restaurant_dict_%s.json'%self.rest_num,'w+')
	f.write(json.dumps(rest_dic,indent = 4, cls=NoIndentEncoder))

        if self.testing == True:
            print "\nrestaurant_dict_%s.json restaurant_dict rendered."%self.rest_num

    def render_senti_statistics(self):
        if self.testing == True:
            print "------------------------------------"
            print "Start rendering sentiment statistics..."
        lexicon = []
        for senti in self.lexicon:
            lexicon.append(senti.replace(' ','-'))

        senti_cnt = 1
        senti_list = []
        for senti in lexicon:
            review_cnt = 1
            senti_frq = 0
            for review in self.backend_reviews:
                senti_frq += review.count(senti)

                if self.testing == True:
                    sys.stdout.write('\rStatus: %s / %s'%(senti_cnt, len(lexicon)))
                    sys.stdout.flush()
                    review_cnt+=1

            orderedDict = OrderedDict()
            orderedDict['index'] = senti_cnt
            orderedDict['word'] = senti
            orderedDict['count'] = senti_frq
            senti_list.append(NoIndent(orderedDict))
            senti_cnt += 1
        f = open('data/sentiment_statistics/restaurant_%s.json'%self.rest_num, 'w+')
        f.write(json.dumps(senti_list, indent = 4, cls=NoIndentEncoder))
        f.close()

        if self.testing == True:
            print 'senti statistic file is rendered.'

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

if __name__ == '__main__':
    parser = new_ReviewParser()
    #parser.render_backend_reviews()
    parser.render_frontend_reviews()
    #parser.render_restaurant_dict()
    #parser.render_senti_statistics()
    print 'Done. restaurant_%s processed.'%sys.argv[1]

