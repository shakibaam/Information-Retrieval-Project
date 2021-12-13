import json
import math
import xlrd
import xlsxwriter
f = open('positional_index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

f = open('non_positional_index.json', encoding='utf-8')
data = json.load(f)
non_positional_index = data
f.close()


data_set = 'IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

number_of_rows = content.nrows

def tfidf_positional():

    for t in positional_index :
        n_t = len(positional_index[t][0])
        print(n_t)


        docs_and_positions = positional_index[t][0]
        for doc in docs_and_positions :
            postings_list = docs_and_positions[doc]

            tf = (1 + math.log10(docs_and_positions[doc][0]))

            idf = math.log10(number_of_rows/n_t)
            # print("idf is {}".format(idf))
            tfidf = tf * idf
            tfidf = float("{:.4f}".format(tfidf))
            print(tfidf)
            docs_and_positions[doc].append(tfidf)


    f = open("tfidf_index.json", "w", encoding="utf-8")
    json.dump(positional_index, f)
    f.close()

def tfidf_non_positional():
    for t in non_positional_index:
        n_t = len(non_positional_index[t])
        # print(n_t)

        docs = non_positional_index[t]
        # print(docs)
        for doc in docs:


            tf = (1 + math.log10(docs[doc]))

            idf = math.log10(number_of_rows / n_t)
            # print("idf is {}".format(idf))
            tfidf = tf * idf
            tfidf = float("{:.4f}".format(tfidf))
            print(tfidf)
            doc_value = (docs[doc] , tfidf)
            docs[doc] = doc_value

    f = open("tfidf_index_non_positional.json", "w", encoding="utf-8")
    json.dump(non_positional_index, f)
    f.close()


# tfidf_non_positional()

f = open('tfidf_index_non_positional.json', encoding='utf-8')
data = json.load(f)
non_positional_index_tfidf = data
f.close()

print(non_positional_index_tfidf)
