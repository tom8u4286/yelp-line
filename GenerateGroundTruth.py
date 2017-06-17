import csv
import sys
import json
import uuid
from operator import itemgetter

class GenerateGroundTruth:
    def __init__(self):
        self.f = open('data/QuestionResult/2A.csv')
        self.raw = [l[2:] for l in list(csv.reader(self.f))]
        self.dishes = [self.raw[0][num*5].strip('1.') for num in range(0,10)]
        self.scores = []

        for num in range(0,10):
            score = 0
            for l in range(1,4):
                for q in range(0,5):
                    score += float(self.raw[l][num*5+q])
            self.scores.append(score)

        lst = []
        for dish, score in zip(self.dishes,self.scores):
            lst.append([score, dish])
        lst = sorted(lst, key=itemgetter(0),reverse=True)
        lst = [NoIndent(l) for l in lst]
        f_out = open('data/GroundTruth/rest2.json','w+')
        f_out.write(json.dumps(lst, indent=4, cls=NoIndentEncoder))

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
    generator = GenerateGroundTruth()

