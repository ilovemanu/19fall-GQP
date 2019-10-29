# Created by alex at 10/4/19

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import csv
import os


def combine_all(input_folder_path):

    dfs = []
    # col_names = ['filename', 'citations', 'circumstance']
    _, _, filenames = next(os.walk(input_folder_path))
    for c in filenames:
        if c.endswith('csv'):
            df = pd.read_csv(os.path.join(input_folder_path, c))
            print(c)
            print(df.shape)
            print(df.head(2))
            dfs.append(df)
    pd_combine = pd.concat(dfs)
    print(pd_combine.shape)
    pd_combine.to_csv(os.path.join(input_folder_path, 'NONs.csv'), index=False)


# if __name__ == '__main__':
#     input_folder_path = '../../all_csv'
#     combine_all(input_folder_path)
    # print(pd.read_csv('../../all_csv/henry_clean.csv').head(2))


def clean_text(input_file_path, output_file_path):
    """
    Clean description of noncompliance.
    :param input_file_path:
    :param output_file_path:
    :return: the output csv contains filename, citations, cleaned description.
    """

    col_names = ['filename', 'citations', 'circumstance']
    raw = pd.read_csv(input_file_path, encoding='utf-8')
    # raw.dropna(axis=0, inplace=True)

    des = raw.paragraph.to_list()
    print(len(des))

    clean_list = []
    for idx, p in enumerate(des):

        # clean line breaks
        temp = re.sub(r'\n', ' ', p.strip().lower())
        # clean special characters
        temp = re.sub(r'[^.,a-z0-9() ]', '', temp)
        # clean title
        # temp = re.sub(r'description(s)? of act(ivity)? or omission constituting noncomplian( )?ce', '', temp)
        temp = re.sub(r'description(s)? of non(compliance)?', '', temp)
        # clean footer/header
        temp = re.sub(r'r\wn(s)? \d{8}', '', temp)
        temp = re.sub(r'enf(\w+)?(.)? doc(\w+)?(.)? no. \d{8}', '', temp)
        # temp = re.sub(r'page \d', '', temp)
        temp = re.sub(r'notice of noncompliance( summary)?', '', temp)
        # remove numbers and punctuations?
        # temp = re.sub(r'[^a-z ]', '', temp)
        # remove multiple spaces
        temp = re.sub(r'\s+', ' ', temp)
        temp = temp.strip()
        # TO-DO correct spells

        print(idx)
        print(temp)
        clean_list.append(temp)

    raw['circumstance'] = clean_list
    raw[['filename', 'citations', 'circumstance']].to_csv(output_file_path, index=False)
    print('Done!')


# if __name__ == '__main__':
#     input_file_path = '../../all_csv/single_293.csv'
#     output_file_path = '../../all_csv/single_293_clean.csv'
#     clean_text(input_file_path, output_file_path)

# input_file_path = '../../parsed/duo_105.csv'
# output_file_path = '../../parsed/duo_105_clean.csv'
# clean_text(input_file_path, output_file_path)
# print(pd.read_csv('../../parsed/duo_105_clean.csv').columns)

# input_file_path = '../../parsed/others_4.csv'
# output_file_path = '../../parsed/others_4_clean.csv'
# clean_text(input_file_path, output_file_path)
# print(pd.read_csv('../../parsed/others_4_clean.csv').columns)


def nlp(file_path):

    raw = pd.read_csv(file_path, encoding='utf-8')
    data = raw.clean.to_list()

    for idx, p in enumerate(data):

        # remove numbers and punctuations
        temp = re.sub(r'[^a-z ]', '', p)
        # remove multiple spaces
        temp = temp.strip()
        temp = re.sub(r'\s+', ' ', temp)

        stop_words = stopwords.words('english')

        word_tokens = nltk.word_tokenize(temp)
        word_tokens = [word for word in word_tokens if word not in stop_words]

        print(idx)
        print(word_tokens)


# input_file_path = 'test.csv'
# nlp(input_file_path)


def utf_8_encoding(input_path):
    """
    Rewrite a csv to have utf-8 encoding.
    :param input_path:
    :return: csv with utf-8 encoding.
    """

    path = input_path

    with open(path, 'r', encoding='utf-8', errors='ignore') as infile, open(path + 'final.csv', 'w') as outfile:

        inputs = csv.reader(infile)
        output = csv.writer(outfile)

        for index, row in enumerate(inputs):
            output.writerow(row)


raw = pd.read_csv('../../all_csv/NONs.csv')
print('')
print(raw.loc[0]['circumstance'])
#
# # temp = [['40,0420'], ['40.1074'], ['40.1003'], ['40.0006'], ['40.0926'], ['40.1074'], ['40.0031'], ['40.1074'],
# #         ['40.1074'], ['40.0034'], ['40.0031'], ['40.0425'], ['40.0835'], ['40.0560'], ['40.0191']]
# idx = raw[raw.citations == "['10.1070']"].index.tolist()
# print(idx)
# raw['citations'].loc[idx] = "['40.1070']"
# raw.to_csv('../../all_csv/NONs.csv', index=False)
# # print(raw[raw.citations == "[]"])
