import json
import math
import xlrd
import xlsxwriter
f = open('index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()


data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

number_of_rows = content.nrows

for t in positional_index :
    n_t = positional_index[t][1]
    docs_and_positions = positional_index[t][0]
    for doc in docs_and_positions :
        postings_list = docs_and_positions[doc]
        tf = (1 + math.log10(docs_and_positions[doc][0]))
        idf = math.log10(number_of_rows/n_t)
        tfidf = tf * idf
        tfidf = float("{:.4f}".format(tfidf))
        print(tfidf)
        docs_and_positions[doc].append(tfidf)


f = open("tfidf_index.json", "w", encoding="utf-8")
json.dump(positional_index, f)
f.close()