import os.path
for num in range(1,265):
    f_back = 'data/backend_reviews/restaurant_%s.txt'%num
    f_front = 'data/frontend_reviews/restaurant_%s.json'%num
    f_dict = 'data/restaurant_dict_list/restaurant_dict_%s.json'%num
    if not os.path.isfile(f_back):
        print 'cannot open file backend_reviews/restaurant_%s.txt'%num
    if not os.path.isfile(f_front):
        print 'cannot open file frontend_reviews/restaurant_%s.json'%num
    if not os.path.isfile(f_dict):
        print 'cannot open file restaurant_dict_list/restaurant_dict_%s.json'%num




