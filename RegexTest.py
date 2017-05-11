import json
import sys

class RegexTest:

    def __init__(self):
        self.rest_num = sys.argv[1]
        self.rest_name, self.rest_id, self.raw_reviews = self.get_rest_info()
        self.raw_dishes = self.get_dishes_info()

    def get_rest_info(self):
        f = open('data/reviews/restaurant_%s.json'%self.rest_num)
        dic = json.load(f)
        return dic['business_name'], dic['business_id'], dic['reviews']

    def get_dishes_info(self):
        f = open('data/restaurant_dict_list/restaurant_dict_%s.json'%self.rest_num)
        dic = json.load(f)
        return [dish['name'] for dish in dic['menu']]

    def count_each_word(self):
        for dish in self.raw_dishes:
            word_list = dish.lower().replace(' & ','').replace(' and ',' ').replace(' or ',' ')
            word_list = word_list.replace(' de ','').replace(' la ',' ').replace(' au ', ' ')
            word_list = word_list.replace(' du ','')
            word_list = word_list.split(' ')
            count_list = []
            if len(word_list) > 1:
                for word in word_list:
                    count = 0
                    for review in self.raw_reviews:
                        count += review.count(word)
                    count_list.append(count)
            print word_list, count_list

if __name__ == '__main__':
    tester = RegexTest()
    tester.count_each_word()
    print 'Done. restaurant_%s.'%sys.argv[1]
