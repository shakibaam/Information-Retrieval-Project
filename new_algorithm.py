from __future__ import unicode_literals
import json
import os
import numpy as np
import parsivar
import xlrd
import xlsxwriter
# from parsivar import *
from hazm import *

data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

data_writer = xlsxwriter.Workbook(data_set)
worksheet = data_writer.add_worksheet()
number_of_rows = content.nrows

normalizer = parsivar.Normalizer(statistical_space_correction=True, date_normalizing_needed=True,
                                 pinglish_conversion_needed=True)
tokenizer = parsivar.Tokenizer()
stemmer = parsivar.FindStems()
stemmer_hazm = Stemmer()

positional_index = dict()
positional_index_with_stops = dict()


def add_to_index(token, position, docID):
    # print(positional_index)

    if token not in positional_index:

        positions = {}
        positions[str(docID)] = []
        positions[str(docID)].append(1)
        positions[str(docID)].append([position])
        print(token + ">>>>>")
        print(positions)

        repeat_num = 1

        dict_value = [positions, repeat_num]
        positional_index[token] = dict_value



    else:
        positions = positional_index[token][0]

        if (str(docID)) in positions:
            positions[str(docID)][1].append(position)
            positions[str(docID)][0] += 1
        else:
            positions[str(docID)] = []
            positions[str(docID)].append(1)
            positions[str(docID)].append([position])

        print(token + ">>>>>")
        print(positions)
        positional_index[token][0] = positions
        positional_index[token][1] += 1


def add_to_index_with_stop(token, position, docID):
    if token not in positional_index_with_stops:

        positions = {}
        positions[str(docID)] = []
        positions[str(docID)].append(1)
        positions[str(docID)].append([position])
        print(token + ">>>>>")
        print(positions)

        repeat_num = 1

        dict_value = [positions, repeat_num]
        positional_index_with_stops[token] = dict_value



    else:
        positions = positional_index_with_stops[token][0]

        if (str(docID)) in positions:
            positions[str(docID)][1].append(position)
            positions[str(docID)][0] += 1
        else:
            positions[str(docID)] = []
            positions[str(docID)].append(1)
            positions[str(docID)].append([position])

        print(token + ">>>>>")
        print(positions)
        positional_index_with_stops[token][0] = positions
        positional_index_with_stops[token][1] += 1


def make_index():
    term_doc = []
    flag =False
    garbage = ['۱','۲','۳','۴','۵','۶','۷','۸','۹','۰','a','b','c','d','e','t','o','p','x','y','z','https','،','.',':','**','-','1','2','3','4','5','6','7','8','9','0','?','**','[',']','(','://','/?','=','&','/','؛']

    for i in range(1, number_of_rows):

        temp = data_reader.sheet_by_index(0).cell(i, 0).value
        temp = normalizer.normalize(temp)

        temp_tokens = tokenizer.tokenize_words(temp)
        print(str(i) + " : " + str(len(temp_tokens)))
        print(temp_tokens)
        for token in temp_tokens:
            term_doc.append((token , i , temp_tokens.index(token)+1))

    for (token , docID , position) in term_doc :

        file = open("stop_words.txt", encoding="utf-8")
        # (listitem in file.read()) and (listitem not in garbage)
        if ((token in file.read()) and (token not in garbage)):
            print("stop :" + token)
            stem_token = stemmer.convert_to_stem(token)
            if "&" in stem_token:
                mazi, mozare = stem_token.split("&")
                # filehandle.write('%s\n' % (mazi + ":" + listitem))
                # filehandle.write('%s\n' % (mozare + ":" + listitem))

                add_to_index_with_stop(mazi, position, docID)
                add_to_index_with_stop(mozare, position, docID)

            else:
                # filehandle.write('%s\n' % (stem_token + ":" + listitem))
                add_to_index_with_stop(stem_token, position, docID)
        else:

            stem_token = stemmer.convert_to_stem(token)
            if "&" in stem_token:
                mazi, mozare = stem_token.split("&")
                # filehandle.write('%s\n' % (mazi + ":" + listitem))
                # filehandle.write('%s\n' % (mozare + ":" + listitem))
                add_to_index(mazi, position, docID)
                add_to_index(mozare, position, docID)
                add_to_index_with_stop(mazi, position, docID)
                add_to_index_with_stop(mozare, position, docID)

            else:
                stem_token = stemmer_hazm.stem(stem_token)
                # filehandle.write('%s\n' % (stem_token + ":" + listitem))
                add_to_index(stem_token, position, docID)
                add_to_index_with_stop(stem_token, position, docID)



        # writing dictionary to file
    f = open("index.json", "w", encoding="utf-8")
    json.dump(positional_index, f)
    f.close()

    f = open("index_with_stops.json", "w", encoding="utf-8")
    json.dump(positional_index_with_stops, f)
    f.close()


# TODO handle searching verbs

def answer_one_word_query(query, positional_index):
    normal_query = normalizer.normalize(query)
    stem_query = stemmer.convert_to_stem(normal_query)

    if stem_query in positional_index:
        print("find some Docs related :)")
        dict_value = positional_index[stem_query]
        docs_and_positions = dict_value[0]

        for doc in docs_and_positions:
            title = data_reader.sheet_by_index(0).cell(int(doc), 2).value
            print(title)


def answer_multi_word_query(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    for token in tokens:
        stem_token = stemmer.convert_to_stem(token)
        if stem_token in positional_index:
            print("find some Docs related :)")
            dict_value = positional_index[stem_token]
            docs_and_positions = dict_value[0]
            for doc in docs_and_positions:
                if doc not in docs:
                    docs[doc] = 1
                else:
                    docs[doc] = docs[doc] + 1

    docs = dict(sorted(docs.items(), key=lambda item: item[1], reverse=True))
    for d in docs:
        title = data_reader.sheet_by_index(0).cell(int(d), 2).value
        print(title)


def main():
    # if (os.stat("index.json").st_size == 0):
    make_index()


# else:
#     # reading dictionary from file
#     f = open('index.json', encoding='utf-8')
#     data = json.load(f)
#     positional_index = data
#     f.close()


# print("1- one word query \n 2- multiple word query")
# num = input()
# if (num == 1):
#     query = input("Enter your one word query")
#     answer_one_word_query(query , positional_index)
# elif (num == 2):
#     query = input("Enter your multiple word query")
#     answer_multi_word_query(query , positional_index)


if __name__ == "__main__":
    main()
