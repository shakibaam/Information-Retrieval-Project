from __future__ import unicode_literals
import json
import os
import parsivar
import xlrd
import xlsxwriter
from hazm import *
f = open('index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

f = open('index_with_stops.json', encoding='utf-8')
data = json.load(f)
positional_index_with_stops = data
f.close()

zifs_ranked_without_stops = dict()
zifs_ranked_with_stops = dict()

for term in positional_index_with_stops :
    if term in positional_index :

        repeat_num = positional_index[term][1]

        zifs_ranked_without_stops[term] = repeat_num

    positions, repeat_num = positional_index_with_stops[term]
    zifs_ranked_with_stops[term] = repeat_num


# sort by their frequencies


zifs_ranked_without_stops = docs = dict(sorted(zifs_ranked_without_stops.items(), key=lambda item: item[1] , reverse=True))
zifs_ranked_with_stops = docs = dict(sorted(zifs_ranked_with_stops.items(), key=lambda item: item[1] , reverse=True))
#

# # without stops
terms = list(zifs_ranked_without_stops.keys())
index = 1
top_frequency =list( zifs_ranked_without_stops.values())[0]
print(top_frequency)
for i in range(31) :

    relative_frequency = "1/{}".format(index)
    zipf_frequency = top_frequency * (1 / index)
    print("word : {} \t actual frequency : {} \t relative_frequency : {} \t zipf_frequency : {} ".format(terms[i],zifs_ranked_without_stops[terms[i]],relative_frequency,zipf_frequency))
    index += 1