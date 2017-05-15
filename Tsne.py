import sys
import numpy as np
import json
import re
import uuid
from collections import OrderedDict
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

class Tsne:

    def __init__(self):
        self.src = sys.argv[1]
        self.array = []
        self.words = []
        self.dim2 = []

    def get_data(self):
        f = open(self.src)
        next(f)
        for line in f :
            vector = line.split(" ")
            self.words.append(vector[0])
            vector = vector[1:-1]
            vector = [float(num) for num in vector]
            self.array.append(vector)

    def dim_deduction(self):
        #pca = PCA(n_components=30)
        #print "pca start.."
        #pca.fit(self.array)
        model = TSNE(n_components=2, random_state=0)
        print "tsne start.."
        self.array = model.fit_transform(self.array)
        #normalizing
        new_max = 0.8
        new_min = -0.8
        old_xs = [vec[0] for vec in self.array]
        old_ys = [vec[1] for vec in self.array]
        min_x = min(old_xs)
        max_x = max(old_xs)
        new_xs = [(new_max-new_min)*(num-min_x)/(max_x-min_x) + new_min for num in old_xs]
        min_y = min(old_ys)
        max_y = max(old_ys)
        new_ys = [(new_max-new_min)*(num-min_y)/(max_y-min_y) + new_min for num in old_ys]
        self.array =[[x,y] for x,y in zip(new_xs,new_ys)]

        total = []
        for i in xrange(len(self.words)):
            line = {}
            line["index"] = i+1
            line["word"] = self.words[i]
            line["vector2"] = list(self.array[i])
            print line
            total.append(NoIndent(line))

        self.dim2 = total

    def render(self):
        filename = sys.argv[1].split("/")
        num = re.search("([0-9]+).+(type[0-9])", filename[3])
        f = open("data/vectors/2dim/restaurant_%s_vector2_%s.json"%(num.group(1),num.group(2)), "w+")
        f.write(json.dumps(self.dim2, indent = 4, cls=NoIndentEncoder))
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

if __name__ == '__main__':
    tsne = Tsne()
    tsne.get_data()
    tsne.dim_deduction()
    tsne.render()
