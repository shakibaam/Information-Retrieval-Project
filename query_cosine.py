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

data_set = 'IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)


number_of_rows = content.nrows

f = open('champions.json', encoding='utf-8')
data = json.load(f)
tokens_and_champions = data
f.close()

f = open('tfidf_index_non_positional.json', encoding='utf-8')
data = json.load(f)
non_positional_index = data
f.close()


def calculate_doc_lenght(doc_id) :
    temp = data_reader.sheet_by_index(0).cell(int(doc_id), 0).value
    temp = hazm_normalaizer.normalize(temp)
    tokens = word_tokenize(temp)
    tokens = [stemmer_hazm.stem(t) for t in tokens]
    length = 0
    for t in tokens :

        length += (non_positional_index[t][doc_id][1]) ** 2 # non_positional_index[t][doc_id][1] is weight of the t in that doc

    return math.sqrt(length)


def query_score (query) :

    query_tokens = word_tokenize(query)
    query_score = {}
    for term, count in Counter(query_tokens).items():
        tf = (1 + math.log10(count))
        idf = math.log10(number_of_rows/1)
        tfidf = tf * idf
        query_score[term] = (tfidf)
    return query_score


def cosine_score_non_positional(query , k):
    scores = dict()
    query = hazm_normalaizer.normalize(query)
    query_tokens = hazm.word_tokenize(query)
    query_scores = query_score(query)
    for i in range(len(query_tokens)):
        wtq = query_scores[query_tokens[i]]

        docs = non_positional_index[stemmer_hazm.stem(query_tokens[i])]
        print(docs)
        for d in docs :
            wtd = docs[d][1]
            if d not in scores :
                scores[d] = wtq * wtd
            else:
                scores[d] += wtq * wtd
    for d in scores :
        scores[d] = scores[d] / calculate_doc_lenght(d)

    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(scores)
    k_first = dict(list(scores.items())[0: k])
    return k_first



def cosine_score_with_champion (query , k) :
    scores = dict()
    query = hazm_normalaizer.normalize(query)
    query_tokens = hazm.word_tokenize(query)
    query_scores = query_score(query)
    for i in range(len(query_tokens)):
        champions = tokens_and_champions[stemmer_hazm.stem(query_tokens[i])]
        wtq = query_scores[query_tokens[i]]

        docs = non_positional_index[stemmer_hazm.stem(query_tokens[i])]
        print(docs)
        for d in champions:
            wtd = docs[d][1]
            if d not in scores:
                scores[d] = wtq * wtd
            else:
                scores[d] += wtq * wtd
    for d in scores:
        scores[d] = scores[d] / calculate_doc_lenght(d)

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
        print("{} : {}".format(d, answers[d]))
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

def make_champion () :
    token_and_champions = dict()
    for t in non_positional_index :

        docs_and_scores = {}
        PL = non_positional_index[t]
        for d in PL :
            docs_and_scores[d] = PL[d][1]
        docs_and_scores = dict(sorted(docs_and_scores.items(), key=lambda item: item[1], reverse=True))
        champions = dict(list(docs_and_scores.items())[0: 40])

        token_and_champions[t] = list(champions.keys())

    f = open("champions.json", "w", encoding="utf-8")
    json.dump(token_and_champions, f)
    f.close()





def main():
    # query = input("Enter your query")
    # answers =  cosine_score_with_champion(query,10)
    # show_answers(answers,query)
    # make_champion(positional_index)
    # make_champion()
    print(len(non_positional_index["امیرکبیر"]))
    print(tokens_and_champions["امیرکبیر"])





if __name__ == "__main__":
    main()
