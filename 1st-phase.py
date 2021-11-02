from __future__ import unicode_literals
import json
import numpy as np
import xlrd
import xlsxwriter
from parsivar import *

data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

data_writer = xlsxwriter.Workbook(data_set)
worksheet = data_writer.add_worksheet()
number_of_rows = content.nrows

normalizer = Normalizer(statistical_space_correction=True , date_normalizing_needed=True , pinglish_conversion_needed=True)
tokenizer = Tokenizer()
stemmer = FindStems()

positional_index = dict()

def add_to_index(token , position , docID):

    if token not in positional_index :
        positions = {}
        positions[str(docID)] = []
        positions[str(docID)].append(position)
        print(token + ">>>>>")
        print(positions)
        each_doc_count = np.zeros(number_of_rows)
        each_doc_count = each_doc_count.tolist()
        each_doc_count [docID] = 1
        repeat_num = 1
        dict_value = [positions , repeat_num , each_doc_count]
        positional_index[token] = dict_value
    else:
        positions = positional_index[token][0]
        each_doc_count = positional_index[token][2]
        positions[str(docID)].append(position)
        print(token + ">>>>>")
        print(positions)
        positional_index[token][0] = positions
        positional_index[token][1] +=1
        each_doc_count[docID] += 1
        positional_index[token][2] = each_doc_count






for i in range(1, number_of_rows+1):

    temp = data_reader.sheet_by_index(0).cell(i, 0).value
    temp = normalizer.normalize(temp)
    worksheet.write(i, 0, temp)

    temp_tokens = tokenizer.tokenize_words(temp)
    print(temp_tokens)
    with open('Tokens.txt', "w", encoding="utf-8") as filehandle:
        for j in range(len(temp_tokens)):
            listitem = temp_tokens[j]
            file = open("stop_words.txt", encoding="utf-8")

            if (listitem in file.read()):
                print("stop :" + listitem)
            else:

                stem_token = stemmer.convert_to_stem(listitem)
                if "&" in stem_token:
                    mazi, mozare = stem_token.split("&")
                    filehandle.write('%s\n' % mazi)
                    filehandle.write('%s\n' % mozare)
                    add_to_index(mazi, j + 1, i)
                    add_to_index(mozare, j + 1, i)

                else:
                    filehandle.write('%s\n' % stem_token)
                    add_to_index(stem_token, j + 1, 2)







#writing dictionary to file
f = open("index.json", "w" , encoding="utf-8")
json.dump(positional_index, f)
f.close()

#reading dictionary from file

f = open('index.json', encoding='utf-8')
data = json.load(f)
print(data['گزارش'])
f.close()



