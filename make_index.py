from __future__ import unicode_literals
import json
import os
import math
import parsivar
import xlrd
import xlsxwriter
from hazm import *
import hazm

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
hazm_normalaizer = hazm.Normalizer()

positional_index = dict()
positional_index_with_stops = dict()
garbage = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰', 'a', 'b', 'c', 'd', 'e', 't', 'o', 'p', 'x', 'y', 'z',
           'https', '،', '.', ':', '**', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?', '**', '[', ']',
           '(', ')', '://', '/?', '=', '&', '/', '؛', '&', '/', '.', '_', '،', '?**', ":", "%", ">>", "<<", "#", "!",
           "*", "«", "»"]


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
            if (position not in positions[str(docID)][1]):
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

    for i in range(1, number_of_rows):

        temp = data_reader.sheet_by_index(0).cell(i, 0).value
        temp = normalizer.normalize(temp)

        temp_tokens = tokenizer.tokenize_words(temp)
        print(str(i) + " : " + str(len(temp_tokens)))
        print(temp_tokens)
        for j in range(len(temp_tokens)):
            term_doc.append((temp_tokens[j], i, j + 1))

    for (token, docID, position) in term_doc:

        file = open("stop_words.txt", encoding="utf-8")
        # (listitem in file.read()) and (listitem not in garbage)
        if ((token in file.read())):
            if ((str(token) not in garbage)):
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

    f = open("index_with_stops.json", "w", encoding="utf-8")
    json.dump(positional_index_with_stops, f)
    f.close()


def answer_one_word_query(query, positional_index):
    normal_query = hazm_normalaizer.normalize(query)
    stem_query = stemmer.convert_to_stem(normal_query)
    f = open("answer.txt", "a", encoding="utf-8")
    i = 0
    if stem_query in positional_index:
        # print("find some Docs related :)")
        dict_value = positional_index[stem_query]
        docs_and_positions = dict_value[0]

        for doc in docs_and_positions:

            title = data_reader.sheet_by_index(0).cell(int(doc), 2).value
            news_content = normalizer.normalize(data_reader.sheet_by_index(0).cell(int(doc), 0).value)
            sentences = sent_tokenize(str(news_content))
            f.write("Title of the news is : {}\n".format(title))
            relative_sentences = [s for s in sentences if query in s]

            print("Title of the news is : {}".format(title))
            #
            # # print(news_content)
            print("senteces which are relative :")
            for s in relative_sentences:
                print(s)
                f.write("{} \n".format(s))
            print("---------------------------------------")


def answer_multi_word_query2(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    f = open("answer.txt", "a", encoding="utf-8")
    # print(tokens)

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
        print(d)
        relative_sentences = []
        title = data_reader.sheet_by_index(0).cell(int(d), 2).value
        news_content = normalizer.normalize(data_reader.sheet_by_index(0).cell(int(d), 0).value)
        sentences = sent_tokenize(str(news_content))
        f.write("Title of the news is : {}\n".format(title))
        for t in tokens:
            relative_sentences += [s for s in sentences if t in s]

        print("Title of the news is : {}".format(title))

        print("senteces which are relative :")
        for s in relative_sentences:
            print(s)
            f.write("{} \n".format(s))
        print("---------------------------------------")


def answer_multi_word_query(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    answers = dict()

    for t in tokens:

        stem_token = stemmer_hazm.stem(t)

        if stem_token in positional_index:
            docs_and_positions = positional_index[stem_token][0]
            # print(docs_and_positions)

            for doc in docs_and_positions:

                positions = docs_and_positions[doc][1]

                i = tokens.index(t) + 1

                count = 1
                if (i == len(tokens)):
                    if doc not in answers:
                      answers[doc] = count

                flag = True
                if i < len(tokens):

                    if doc in positional_index[stemmer_hazm.stem(tokens[i])][0]:
                        # print(doc)
                        # print(positional_index[stemmer_hazm.stem(tokens[i])][0][doc][1])
                        # print(positions)
                        while flag:

                            find = False
                            if doc in positional_index[stemmer_hazm.stem(tokens[i])][0]:
                                print(tokens[i])
                                print(t)
                                for p1 in positions:
                                    for p2 in positional_index[stemmer_hazm.stem(tokens[i])][0][doc][1]:
                                        distance = abs(p1 - p2)
                                        if distance == i - tokens.index(t):
                                            print(p1)
                                            print(p2)
                                            find = True
                                if find == True:
                                    print(doc)
                                    print("here1")
                                    print("=============================")
                                    count += 1
                                    if ( doc in answers and answers[doc] < count):
                                       answers[doc] = count
                                    elif doc not  in answers :
                                        answers[doc] = count
                                    # print(answers[doc])
                                    i += 1
                                    if i == len(tokens):
                                        flag = False
                                    else:
                                        continue



                                else:
                                    print("here2")
                                    print("=============================")
                                    if (doc in answers and answers[doc] < count):
                                        answers[doc] = count
                                    elif doc not in answers:
                                        answers[doc] = count


                                    flag = False

                            else:flag = False


    answers = dict(sorted(answers.items(), key=lambda item: item[1], reverse=True))
    print(answers)
    file_name = str(query) + ".txt"
    f = open(file_name, "a", encoding="utf-8")
    for d in answers:
        print(d)
        relative_sentences = []
        title = data_reader.sheet_by_index(0).cell(int(d), 2).value
        news_content = hazm_normalaizer.normalize(data_reader.sheet_by_index(0).cell(int(d), 0).value)
        sentences = sent_tokenize(str(news_content))
        # f.write("Title of the news is : {}\n".format(title))
        for t in tokens:
            relative_sentences += [s for s in sentences if t in s]

        print("Title of the news is : {}".format(title))
        f.write("Title of the news is : {}\n".format(title))

        print("senteces which are relative :")
        for s in relative_sentences:
            print(s)

            f.write("{} \n".format(s))
        f.write("-----------------------------------------------------------------------------------------\n")
        print("---------------------------------------")


def answer_multi_word_query3(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    answers = dict()

    for t in tokens:

        stem_token = stemmer_hazm.stem(t)
        # print(positional_index["واکسن"][0])
        # print(positional_index["آسترازنکا"][0])

        if stem_token in positional_index:
            docs_and_positions = positional_index[stem_token][0]
            # print(t)
            # print(docs_and_positions)

            for doc in docs_and_positions:

                positions = docs_and_positions[doc][1]

                # print("{}  {}  {}".format(stem_token,doc,positions))

                i = tokens.index(t) + 1
                count = 1
                answers[doc] = count

                flag = True
                if i < len(tokens):

                    if doc in positional_index[tokens[i]][0]:
                        while flag:

                            j = 0

                            j_flag = True
                            k = 0
                            k_flag = True

                            find = False
                            # for p1 in positions :
                            #     for p2 in positional_index[tokens[i]][0][doc][1] :

                            while j_flag:

                                while k_flag:

                                    # distance = int(positional_index[tokens[i]][0][doc][1][k])
                                    distance = abs(positions[j] - positional_index[tokens[i]][0][doc][1][k])
                                    # distance = positional_index[tokens[i]][0][doc][1][k] - positions[j]
                                    print(distance)

                                    # if distance >i - tokens.index(t) :
                                    #     j += 1
                                    #     k = 0

                                    if distance == i - tokens.index(t):
                                        find = True
                                        # j_flag = False
                                        # k_flag = False
                                    k += 1
                                    if k >= len(positional_index[tokens[i]][0][doc][1]):
                                        k_flag = False
                                        j_flag = False
                                    else:
                                        continue
                                    j += 1
                                    if j >= len(positions):
                                        j_flag = False
                                        k_flag = False
                                    else:
                                        continue

                            # distances = [x2 - x1 for x2, x1 in zip(positional_index[tokens[i]][0][doc], positions)]
                            if find == True:
                                print("here1")
                                print("=============================")
                                count += 1
                                answers[doc] = count
                                i += 1
                                if i == len(tokens):
                                    flag = False

                            else:
                                print("here2")
                                print("=============================")
                                answers[doc] = count
                                flag = False
                    # answers[doc] = count

                    # else:
                    #     flag = False

    answers = dict(sorted(answers.items(), key=lambda item: item[1], reverse=True))
    print(answers)
    # for d in answers:
    #     relative_sentences = []
    #     title = data_reader.sheet_by_index(0).cell(int(d), 2).value
    #     news_content = hazm_normalaizer.normalize(data_reader.sheet_by_index(0).cell(int(d), 0).value)
    #     sentences = sent_tokenize(str(news_content))
    #     # f.write("Title of the news is : {}\n".format(title))
    #     for t in tokens:
    #         relative_sentences += [s for s in sentences if t in s]
    #
    #     print("Title of the news is : {}".format(title))
    #
    #     print("senteces which are relative :")
    #     for s in relative_sentences:
    #         print(s)
    #         # f.write("{} \n".format(s))
    #     print("---------------------------------------")


def main():
    # if (os.stat("index.json").st_size == 0):
    #     make_index()

    # else:
    # reading dictionary from file
    f = open('positional_index.json', encoding='utf-8')
    data = json.load(f)
    positional_index = data
    f.close()

    # stop_words = [word for word in open('stop_words.txt', 'r', encoding='utf8').read().split('\n')]
    # for word in stop_words:
    #     if word in positional_index :
    #
    #         positional_index.pop(word)
    # for x in garbage :
    #     if x in positional_index :
    #         positional_index.pop(x)
    # f = open("positional_index.json", "w", encoding="utf-8")
    # json.dump(positional_index, f)
    # f.close()

    # f = open('index_with_stops.json', encoding='utf-8')
    # data = json.load(f)
    # positional_index_with_stops = data
    # f.close()
    #
    # for x in garbage :
    #     if x in positional_index_with_stops :
    #         positional_index_with_stops.pop(x)

    # f = open("positional_index.json", "w", encoding="utf-8")
    # json.dump(positional_index, f)
    # f.close()
    # f = open("positional_index_with_stops.json", "w", encoding="utf-8")
    # json.dump(positional_index_with_stops, f)
    # f.close()

    print("1- one word query \n 2- multiple word query")
    num = input()
    if (int(num) == 1):
        query = input("Enter your one word query")
        answer_one_word_query(query, positional_index)
    elif (int(num) == 2):
        query = input("Enter your multiple word query")
        answer_multi_word_query(query, positional_index)


if __name__ == "__main__":
    main()
