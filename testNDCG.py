import json
import sys
import numpy as np
from operator import itemgetter


class NDCG:

    def __init__(self):
        self.ground_truth = json.load(open('data/GroundTruth/rest1.json'))
        self.dishes = json.load(open('data/restaurant_dict_list/restaurant_dict_1.json'))['menu']
        self.ground_truth_ar = [d['name_ar'] for dish in self.ground_truth for d in self.dishes if dish[1]==d['name']]
        self.rank_dish_list = json.load(open('data/rank/restaurant_1_rank_type3.json'))['rank']

    def ndcg_ours(self):
        method_list = []
        for d in self.ground_truth_ar:
            for dish in self.rank_dish_list:
                if dish['dish'] == d:
                    method_list.append([dish['rank_by_sum_higher0_cos_zXnorm_frq'],dish['dish']])
        method_list = sorted(method_list, key=itemgetter(0))

        print '-----------------------------'
        print 'method:'
        for d in method_list:
            print d
        print 'gt:'
        for d in self.ground_truth_ar:
            print d

        i = [4,4,3,3,2,2,1,1,0,0]
        r = []
        for dish in method_list:
            for num, d in zip(i, self.ground_truth_ar):
                if dish[1] == d:
                    r.append(num)
        print 'r:', r
        print 'ndcg@10:',self.ndcg_at_k(r, 10, method=0)

    def ndcg_frq(self):
        frq_list = []
        for d in self.ground_truth_ar:
            for dish in self.rank_dish_list:
                if dish['dish'] == d:
                    frq_list.append([dish['rank_by_frq'],dish['dish']])
        frq_list = sorted(frq_list, key=itemgetter(0))

        print '-----------------------------'
        print 'frq:'
        for d in frq_list:
            print d
        print 'gt:'
        for d in self.ground_truth_ar:
            print d

        i = [4,4,3,3,2,2,1,1,0,0]
        r = []
        for dish in frq_list:
            for num, d in zip(i, self.ground_truth_ar):
                if dish[1] == d:
                    r.append(num)
        print 'r:', r
        print 'ndcg@10:',self.ndcg_at_k(r, 10, method=0)

    def dcg_at_k(self, r, k, method=0):
        """Score is discounted cumulative gain (dcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> dcg_at_k(r, 1)
        3.0
        >>> dcg_at_k(r, 1, method=1)
        3.0
        >>> dcg_at_k(r, 2)
        5.0
        >>> dcg_at_k(r, 2, method=1)
        4.2618595071429155
        >>> dcg_at_k(r, 10)
        9.6051177391888114
        >>> dcg_at_k(r, 11)
        9.6051177391888114
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Discounted cumulative gain
        """
        r = np.asfarray(r)[:k]
        if r.size:
            if method == 0:
                return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
            elif method == 1:
                return np.sum(r / np.log2(np.arange(2, r.size + 2)))
            else:
                raise ValueError('method must be 0 or 1.')
        return 0.

    def ndcg_at_k(self,r, k, method=0):
        """Score is normalized discounted cumulative gain (ndcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> ndcg_at_k(r, 1)
        1.0
        >>> r = [2, 1, 2, 0]
        >>> ndcg_at_k(r, 4)
        0.9203032077642922
        >>> ndcg_at_k(r, 4, method=1)
        0.96519546960144276
        >>> ndcg_at_k([0], 1)
        0.0
        >>> ndcg_at_k([1], 2)
        1.0
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Normalized discounted cumulative gain
        """
        dcg_max = self.dcg_at_k(sorted(r, reverse=True), k, method)
        if not dcg_max:
            return 0.
        return self.dcg_at_k(r, k, method) / dcg_max

if __name__ == '__main__':
    test = NDCG()
    test.ndcg_frq()
    sys.exit()

