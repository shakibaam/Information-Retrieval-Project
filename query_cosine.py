import json
from hazm import *
import hazm
import parsivar
import math
from collections import Counter
import xlrd
import xlsxwriter

hazm_normalaizer = hazm.Normalizer()
tokenizer = parsivar.Tokenizer()
normalizer = parsivar.Normalizer(statistical_space_correction=True, date_normalizing_needed=True,pinglish_conversion_needed=True)
stemmer_hazm = Stemmer()

data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)


number_of_rows = content.nrows

f = open('tfidf_index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

f = open('with_champion_index.json', encoding='utf-8')
data = json.load(f)
positional_index_with_champion = data
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




def cosine_score (query , k) :
    scores = dict()
    query_tokens = tokenizer.tokenize_words(query)
    query_scores = query_score(query)
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
    print(scores)
    k_first = dict(list(scores.items())[0: k])
    return k_first

def cosine_score_with_champion (query , k) :
    scores = dict()
    query_tokens = tokenizer.tokenize_words(query)
    query_scores = query_score(query)
    for i in range(len(query_tokens)):
        wtq = query_scores [i]
        docs_and_positions = positional_index_with_champion[query_tokens[i]][0]
        champions = positional_index_with_champion[query_tokens[i]][2]
        for doc in champions :
            wtd = docs_and_positions[doc][2]
            if doc not in scores :
                scores[doc] = wtq * wtd
            else:
                scores[doc] += wtq * wtd


    for d in scores :
        scores[d] = scores[d]/len(scores)

    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(scores)
    k_first = dict(list(scores.items())[0: k])
    return k_first


def show_answers(answers,query):
    file_name = str(query) + ".txt"
    f = open(file_name, "a", encoding="utf-8")
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    for d in answers:
        print(d)
        relative_sentences = []
        title = data_reader.sheet_by_index(0).cell(int(d), 2).value
        news_content = hazm_normalaizer.normalize(data_reader.sheet_by_index(0).cell(int(d), 0).value)
        sentences = sent_tokenize(str(news_content))

        for t in tokens:
            for s in sentences:
                if stemmer_hazm.stem(t) in s:
                    if s not in relative_sentences:
                        relative_sentences.append(s)

        print("Title of the news is : {}".format(title))
        f.write("Title of the news is : {}\n".format(title))

        print("senteces which are relative :")
        for s in relative_sentences:
            print(s)

            f.write("{} \n".format(s))
        f.write("-----------------------------------------------------------------------------------------\n")

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



def main():
    query = input("Enter your query")
    answers =  cosine_score_with_champion(query,10)
    show_answers(answers,query)
    # make_champion(positional_index)


if __name__ == "__main__":
    main()
