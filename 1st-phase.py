from __future__ import unicode_literals
from collections import defaultdict
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
each_word_doc = dict()

for i in range(1, number_of_rows+1):


    temp = data_reader.sheet_by_index(0).cell(i, 0).value
    temp = normalizer.normalize(temp)
    worksheet.write(i, 0, temp)

    temp_tokens = tokenizer.tokenize_words(temp)
    print(temp_tokens)
    with open('Tokens.txt', "w", encoding="utf-8") as filehandle:
        for listitem in temp_tokens:
            file = open("stop_words.txt" , encoding="utf-8")

            if (listitem in file.read()):
                print("stop :" + listitem)
            else:

                stem_token = stemmer.convert_to_stem(listitem)
                if "&" in stem_token :
                    mazi , mozare = stem_token.split("&")
                    filehandle.write('%s\n' % mazi)
                    filehandle.write('%s\n' % mozare)
                else:
                    filehandle.write('%s\n' % stem_token)




def add_to_index(token , position , docID):

    if token not in positional_index :
        positions = defaultdict()
        positions[docID].append(position)
        repeat_num = 1
        dict_value = [positions , repeat_num]
        positional_index[token] = dict_value
    else:
        positions = positional_index[token][0]
        positions[docID].append(position)
        positional_index[token][0] = positions
        positional_index[token][1] +=1
        #TODO each_word_doc update



