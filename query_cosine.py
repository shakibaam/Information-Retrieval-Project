import json

import parsivar
import math
from collections import Counter
import xlrd
import xlsxwriter


tokenizer = parsivar.Tokenizer()

data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

data_writer = xlsxwriter.Workbook(data_set)
worksheet = data_writer.add_worksheet()
number_of_rows = content.nrows

f = open('index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

def query_score (query) :
    query_tokens = tokenizer.tokenize_words(query)
    query_score = []
    for term, count in Counter(query_tokens).items():
        tf = (1 + math.log10(count))
        idf = math.log10(number_of_rows/1)
        tfidf = tf * idf
        query_score.append(tfidf)
    return query_score




def cosine_score (query , query_scores , k) :
    scores = dict()
    query_tokens = tokenizer.tokenize_words(query)
    for i in range(len(query_tokens)):
        wtq = query_scores [i]
        docs_and_positions = positional_index[query_tokens[i]][0]
        for doc in docs_and_positions :
            wtd = docs_and_positions[doc][2]
            if doc not in scores :
                scores[doc] = wtq * wtd
            else:
                scores[doc] += wtq * wtd


    for d in scores :
        scores[d] = scores[d]/len(scores)

    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    k_first = dict(list(scores.items())[0: k])
    return k_first


def make_champion (positional_index) :
    for t in positional_index :
        n_t = positional_index[t][1]
        docs_and_positions = positional_index[t][0]
        # r_champion = math.ceil(n_t/2)
        champions = []

        # find w max
        docs = list(docs_and_positions)
        w_max = docs_and_positions[docs[0]][2]
        for doc in docs_and_positions :
            wtd = docs_and_positions[doc][2]
            if wtd >= w_max :
                w_max = wtd

        for doc in docs_and_positions :
            wtd = docs_and_positions[doc][2]
            if wtd > w_max/2 :
                champions.append(doc)

        positional_index[t].append(champions)





f = open("with_champion_index.json", "w", encoding="utf-8")
json.dump(positional_index, f)
f.close()