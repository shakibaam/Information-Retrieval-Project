from __future__ import unicode_literals

import json
import math
import numpy as np
import parsivar
import xlrd
import xlsxwriter
import matplotlib.pyplot as plt
# from parsivar import *
from hazm import *

data_set = 'D:\ترم7\بازیابی\Project-1st Phase\IR-1st-Phase\IR1_7k_news.xlsx'
data_reader = xlrd.open_workbook(data_set)
content = data_reader.sheet_by_index(0)

data_writer = xlsxwriter.Workbook(data_set)
worksheet = data_writer.add_worksheet()
number_of_rows = content.nrows

# normalizer = parsivar.Normalizer(statistical_space_correction=True, date_normalizing_needed=True,
#                                  pinglish_conversion_needed=True)
tokenizer = parsivar.Tokenizer()
stemmer = parsivar.FindStems()
stemmer_hazm = Stemmer()
normalizer = Normalizer()

positional_index = dict()
positional_index_with_stops = dict()
garbage = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰', 'a', 'b', 'c', 'd', 'e', 't', 'o', 'p', 'x', 'y', 'z',
           'https', '،', '.', ':', '**', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?', '**', '[', ']',
           '(', ')', '://', '/?', '=', '&', '/', '؛', '&', '/', '.', '_', '،', '?**', ":"]

all_token = 2590736


def count_term_stemm(tokens, terms_num, terms):
    count = 0
    if len(terms_num) != 0:
        count = terms_num[-1]
    for token in tokens:

        stem_token = stemmer.convert_to_stem(token)
        if "&" in stem_token:
            mazi, mozare = stem_token.split("&")

            if mazi not in terms:
                terms.append(mazi)
                count += 1
            if mozare not in terms:
                terms.append(mozare)
                count += 1
        else:
            stem_token = stemmer_hazm.stem(stem_token)

            if stem_token not in terms:
                terms.append(stem_token)
                count += 1
    terms_num.append(count)
    return terms_num, terms


def count_term_no_stemm(tokens, terms_num, terms):
    count = 0
    if len(terms_num) != 0:
        count = terms_num[-1]
    for token in tokens:
        terms.append(token)
        count += 1
    terms_num.append(count)
    return terms_num, terms


# for stemming case
heaps_tokens_num = []
heaps_tokens = []
heaps_terms = []
terms_num = []
token_num = 0
for i in range(1, 2001):
    #
    temp = data_reader.sheet_by_index(0).cell(i, 0).value
    temp = normalizer.normalize(temp)

    temp_tokens = tokenizer.tokenize_words(temp)
    if (i == 500 or i == 1000 or i == 1500 or i == 2000):
        token_num += len(temp_tokens)
        heaps_tokens += temp_tokens
        terms_num, heaps_terms = count_term_stemm(heaps_tokens, terms_num, heaps_terms)
        heaps_tokens_num.append(token_num)
        heaps_tokens = []

    else:
        token_num += len(temp_tokens)
        heaps_tokens += temp_tokens

f = open('index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

x = np.array(heaps_tokens_num)
y = np.array(terms_num)
log_token = np.log10(x)
log_term = np.log10(y)
b, k = np.polyfit(log_token, log_term, 1)
dic_predict = math.pow(10, k) * math.pow(all_token, b)
print("For stemming case")
print(" b is = {} and k is = {}".format(b, k))
print("Predicted size for dictionary is {}".format(dic_predict))
print("Real size for dictionary is {}".format(len(positional_index)))
plt.plot(log_token, log_term)
plt.plot(log_token, b * log_token + k)
plt.xlabel("Total tokens")
plt.ylabel("Distinct words")
plt.show()

# for non stemming case
heaps_tokens_num = []
heaps_tokens = []
heaps_terms = []
terms_num = []
token_num = 0
for i in range(1, 2001):
    #
    temp = data_reader.sheet_by_index(0).cell(i, 0).value
    temp = normalizer.normalize(temp)

    temp_tokens = tokenizer.tokenize_words(temp)
    if (i == 500 or i == 1000 or i == 1500 or i == 2000):
        token_num += len(temp_tokens)
        heaps_tokens += temp_tokens
        terms_num, heaps_terms = count_term_no_stemm(heaps_tokens, terms_num, heaps_terms)
        heaps_tokens_num.append(token_num)
        heaps_tokens = []

    else:
        token_num += len(temp_tokens)
        heaps_tokens += temp_tokens

# def main():

f = open('index.json', encoding='utf-8')
data = json.load(f)
positional_index = data
f.close()

x = np.array(heaps_tokens_num)
y = np.array(terms_num)
log_token = np.log10(x)
log_term = np.log10(y)
b, k = np.polyfit(log_token, log_term, 1)
dic_predict = math.pow(10, k) * math.pow(all_token, b)
print("For non stemming case")
print(" b is = {} and k is = {}".format(b, k))
print("Predicted size for dictionary is {}".format(dic_predict))
print("Real size for dictionary is {}".format(len(positional_index)))
plt.plot(log_token, log_term)
plt.plot(log_token, b * log_token + k)
plt.xlabel("Total tokens")
plt.ylabel("Distinct words")
plt.show()
