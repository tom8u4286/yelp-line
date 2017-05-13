import os.path
from os import listdir

print 'file num data/backend_reviews/ :' , len(listdir('data/backend_reviews/'))
print 'file num data/compare/ :' , len(listdir('data/compare/'))
print 'file num data/cooccurrence/ :' , len(listdir('data/cooccurrence/'))
print 'file num data/frontend_reviews/ :' , len(listdir('data/frontend_reviews/'))
print 'file num data/rank/ :' , len(listdir('data/rank/'))
print 'file num data/restaurant_dict_list/ :' , len(listdir('data/restaurant_dict_list/'))
print 'file num data/reviews/ :' , len(listdir('data/reviews/'))
print 'file num data/senitment_statistics/ :' , len(listdir('data/sentiment_statistics/'))
print 'file num data/vectors/64dim/ :' , len(listdir('data/vectors/64dim/'))
print 'file num data/vectors/norm_64dim/ :', len(listdir('data/vectors/norm_64dim/'))
print 'file num data/voc/ :', len(listdir('data/voc/'))
print '----------------------------------------------'

for num in range(1,257):
    f_back = 'data/backend_reviews/restaurant_%s.txt'%num
    f_compare = 'data/compare/restaurant_%s.json'%num
    f_coo = 'data/cooccurrence/restaurant_%s_cooccur_type3.txt'%num
    f_front = 'data/frontend_reviews/restaurant_%s.json'%num
    f_dict = 'data/restaurant_dict_list/restaurant_dict_%s.json'%num
    f_rank = 'data/rank/restaurant_%s_rank_type3.json'%num
    f_senti = 'data/sentiment_statistics/restaurant_%s.json'%num
    f_64dim = 'data/vectors/64dim/restaurant_%s_vector64_type3.txt'%num
    f_n64dim = 'data/vectors/norm_64dim/norm_restaurant_%s_vector64_type3.txt'%num
    f_voc = 'data/voc/restaurant_%s_voc.txt'%num

    checkList = [f_back, f_compare, f_coo, f_front, f_dict, f_rank, f_senti, f_64dim, f_n64dim, f_voc]

    for f in checkList:
        if not os.path.isfile(f):
            print "file %s doesn't exist."%f



