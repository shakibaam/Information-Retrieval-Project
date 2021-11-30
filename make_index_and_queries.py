from __future__ import unicode_literals
import json
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
lemmatizer = hazm.Lemmatizer()
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

        if ((token in file.read())):
            if ((str(token) not in garbage)):
                print("stop :" + token)
                stem_token = stemmer.convert_to_stem(token)
                if "&" in stem_token:
                    mazi, mozare = stem_token.split("&")

                    add_to_index_with_stop(mazi, position, docID)
                    add_to_index_with_stop(mozare, position, docID)

                else:

                    add_to_index_with_stop(stem_token, position, docID)
        else:

            stem_token = stemmer.convert_to_stem(token)
            if "&" in stem_token:
                mazi, mozare = stem_token.split("&")

                add_to_index(mazi, position, docID)
                add_to_index(mozare, position, docID)
                add_to_index_with_stop(mazi, position, docID)
                add_to_index_with_stop(mozare, position, docID)

            else:
                stem_token = stemmer_hazm.stem(stem_token)

                add_to_index(stem_token, position, docID)
                add_to_index_with_stop(stem_token, position, docID)

        # writing dictionary to file

    f = open("index_with_stops.json", "w", encoding="utf-8")
    json.dump(positional_index_with_stops, f)
    f.close()


def answer_multi_word_query(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    answers = dict()

    for t in tokens:

        stem_token = stemmer_hazm.stem(t)

        if stem_token in positional_index:
            docs_and_positions = positional_index[stem_token][0]
            print(docs_and_positions)

            for doc in docs_and_positions:

                positions = docs_and_positions[doc][1]

                i = tokens.index(t) + 1

                count = 1
                if (i == len(tokens)):
                    if doc not in answers:
                        answers[doc] = count

                flag = True
                test = False
                if i < len(tokens):

                    if doc in positional_index[stemmer_hazm.stem(tokens[i])][0]:

                        while flag:

                            find = False

                            if doc in positional_index[stemmer_hazm.stem(tokens[i])][0]:
                                print(tokens[i])
                                print(t)
                                for p1 in positions:
                                    for p2 in positional_index[stemmer_hazm.stem(tokens[i])][0][doc][1]:
                                        distance = abs(p1 - p2)
                                        if distance == i - tokens.index(t):
                                            if test:
                                                if p1 == pos1:
                                                    print(p1)
                                                    print(p2)
                                                    pos1 = p1
                                                    pos2 = p2
                                                    find = True
                                            else:
                                                print(p1)
                                                print(p2)
                                                pos1 = p1
                                                pos2 = p2
                                                find = True

                                if find == True:
                                    print(doc)
                                    print("here1")
                                    print("=============================")
                                    count += 1
                                    if (doc in answers and answers[doc] < count):
                                        answers[doc] = count
                                    elif doc not in answers:
                                        answers[doc] = count
                                    # print(answers[doc])
                                    i += 1
                                    if i == len(tokens):
                                        flag = False
                                    else:
                                        test = True
                                        continue



                                else:
                                    print("here2")
                                    print("=============================")
                                    if (doc in answers and answers[doc] < count):
                                        answers[doc] = count
                                    elif doc not in answers:
                                        answers[doc] = count

                                    flag = False

                            else:
                                flag = False
                    else:
                        if doc not in answers:
                            answers[doc] = count
                        if doc in answers and answers[doc] < count:
                            answers[doc] = count

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
            for s in sentences:
                if stemmer_hazm.stem(t) in s:
                    if s not in relative_sentences:
                        relative_sentences.append(s)
            # relative_sentences += [s for s in sentences if t in s]

        print("Title of the news is : {}".format(title))
        f.write("Title of the news is : {}\n".format(title))

        print("senteces which are relative :")
        for s in relative_sentences:
            print(s)

            f.write("{} \n".format(s))
        f.write("-----------------------------------------------------------------------------------------\n")
        print("---------------------------------------")


def answer_multi_word_query2(query, positional_index):
    docs = dict()
    normal_query = normalizer.normalize(query)
    tokens = tokenizer.tokenize_words(normal_query)
    answers = dict()

    for t in tokens:

        stem_token = stemmer.convert_to_stem(t)
        if "&" not in stem_token:

            if stem_token in positional_index:
                docs_and_positions = positional_index[stem_token][0]
                print(docs_and_positions)

                for doc in docs_and_positions:

                    positions = docs_and_positions[doc][1]

                    i = tokens.index(t) + 1

                    count = 1
                    if (i == len(tokens)):
                        if doc not in answers:
                            answers[doc] = count

                    flag = True
                    test = False
                    if i < len(tokens):

                        if doc in positional_index[stemmer.convert_to_stem(tokens[i])][0]:

                            while flag:

                                find = False

                                if doc in positional_index[stemmer.convert_to_stem(tokens[i])][0]:
                                    print(tokens[i])
                                    print(t)
                                    for p1 in positions:
                                        for p2 in positional_index[stemmer.convert_to_stem(tokens[i])][0][doc][1]:
                                            distance = abs(p1 - p2)
                                            if distance == i - tokens.index(t):
                                                if test:
                                                    if p1 == pos1:
                                                        print(p1)
                                                        print(p2)
                                                        pos1 = p1
                                                        pos2 = p2
                                                        find = True
                                                else:
                                                    print(p1)
                                                    print(p2)
                                                    pos1 = p1
                                                    pos2 = p2
                                                    find = True

                                    if find == True:
                                        print(doc)
                                        print("here1")
                                        print("=============================")
                                        count += 1
                                        if (doc in answers and answers[doc] < count):
                                            answers[doc] = count
                                        elif doc not in answers:
                                            answers[doc] = count
                                        # print(answers[doc])
                                        i += 1
                                        if i == len(tokens):
                                            flag = False
                                        else:
                                            test = True
                                            continue



                                    else:
                                        print("here2")
                                        print("=============================")
                                        if (doc in answers and answers[doc] < count):
                                            answers[doc] = count
                                        elif doc not in answers:
                                            answers[doc] = count

                                        flag = False

                                else:
                                    flag = False
                        else:
                            if doc not in answers:
                                answers[doc] = count
                            if doc in answers and answers[doc] < count:
                                answers[doc] = count
        else:

            verb_stems = stem_token.split("&")
            print(verb_stems)
            for v in verb_stems:
                if v in positional_index:

                    docs_and_positions = positional_index[v][0]
                    print(docs_and_positions)

                    for doc in docs_and_positions:

                        positions = docs_and_positions[doc][1]

                        i = tokens.index(t) + 1

                        count = 1
                        if (i == len(tokens)):
                            if doc not in answers:
                                answers[doc] = count

                        flag = True
                        test = False
                        if i < len(tokens):

                            if doc in positional_index[stemmer.convert_to_stem(tokens[i])][0]:

                                while flag:

                                    find = False

                                    if doc in positional_index[stemmer.convert_to_stem(tokens[i])][0]:
                                        print(tokens[i])
                                        print(t)
                                        for p1 in positions:
                                            for p2 in positional_index[stemmer.convert_to_stem(tokens[i])][0][doc][1]:
                                                distance = abs(p1 - p2)
                                                if distance == i - tokens.index(t):
                                                    if test:
                                                        if p1 == pos1:
                                                            print(p1)
                                                            print(p2)
                                                            pos1 = p1
                                                            pos2 = p2
                                                            find = True
                                                    else:
                                                        print(p1)
                                                        print(p2)
                                                        pos1 = p1
                                                        pos2 = p2
                                                        find = True

                                        if find == True:
                                            print(doc)
                                            print("here1")
                                            print("=============================")
                                            count += 1
                                            if (doc in answers and answers[doc] < count):
                                                answers[doc] = count
                                            elif doc not in answers:
                                                answers[doc] = count
                                            # print(answers[doc])
                                            i += 1
                                            if i == len(tokens):
                                                flag = False
                                            else:
                                                test = True
                                                continue



                                        else:
                                            print("here2")
                                            print("=============================")
                                            if (doc in answers and answers[doc] < count):
                                                answers[doc] = count
                                            elif doc not in answers:
                                                answers[doc] = count

                                            flag = False

                                    else:
                                        flag = False
                            else:
                                if doc not in answers:
                                    answers[doc] = count
                                if doc in answers and answers[doc] < count:
                                    answers[doc] = count

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
        print("---------------------------------------")


def main():
    # if (os.stat("index.json").st_size == 0):
    #     make_index()

    # else:
    # reading dictionary from file
    f = open('index.json', encoding='utf-8')
    data = json.load(f)
    positional_index = data
    f.close()

    print(positional_index["رفت"])
    query = input("Enter your  query")
    answer_multi_word_query2(query, positional_index)


if __name__ == "__main__":
    main()
