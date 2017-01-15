import json, sys, uuid, scipy, os, math, re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import itertools


"""open the file of vector200,let sys.argv[1] = data/line-data/vectors/norm_200dim/norm_restaurant_1_vector200.txt"""
f_vec200 = open(sys.argv[1])
length = int(next(f_vec200).split(" ")[0])

"""render the vectors list and unique words list."""
words = []
vectors = []
for line in f_vec200:
    word_vec = line.split(" ")
    word = word_vec[0]
    #print word_vec[1:-1][199]
    vec = [float(num) for num in word_vec[1:-1]]

    words.append(word)
    vectors.append(vec)

"""render the cooccurrece matrix"""
coo_file_name = "../data/line-data/cooccurrence/restaurant_%s_cooccur.txt"%re.search("[0-9]+",sys.argv[1].split("_")[3]).group(0)
f_coo = open(coo_file_name)

coo_matrix = np.zeros((length,length))
print "rendering coo_matrix..."
cnt = 0
total = int(sum(1 for _ in f_coo))
f_coo = open(coo_file_name)
for line in f_coo:
    cnt += 1
    line_list = line.split(" ")
    index1 = words.index(line_list[0])
    index2 = words.index(line_list[1])
    coo_matrix[index1][index2] = line_list[2]

    sys.stdout.write("\rStatus: %s / %s"%(cnt,total))
    sys.stdout.flush()
coo_matrix = coo_matrix.flatten()
print "\ncoo_matrix size: ",coo_matrix.size
#print coo_matrix[words.index("scold")][words.index("manner")]
"""test matrix"""
#test_words = ["apple","pineapple","orange"]
#test_vectors = [ [1,1], [-1,-1], [1,0]]
#test_coo = ["apple pineapple 1","apple orange 2","pineapple apple 1","orange apple 2","pineapple orange 3", "orange pineapple 3"]
#coo_matrix = np.zeros((3,3))
#print coo_matrix


"""render the cosine matrix"""
A = np.array(vectors)
cos_matrix = cosine_similarity(A)
cos_matrix = cos_matrix.flatten()
print "cos_matrix size: ",cos_matrix.size

"""render the dot matrix"""
dot_matrix = A.dot(A.T)
dot_matrix = dot_matrix.flatten()
print "dot_matrix size: ",dot_matrix.size

"""render the correlations."""
print "coo and cos: ", np.corrcoef(coo_matrix, cos_matrix)
print "coo and dot: ", np.corrcoef(coo_matrix, dot_matrix)


