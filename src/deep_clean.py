# Created by alex at 10/4/19

import pandas as pd
import re
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

    des = raw.circumstance.to_list()
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
#     input_file_path = '../../uao.csv'
#     output_file_path = '../../uao_clean.csv'
#     clean_text(input_file_path, output_file_path)

# input_file_path = '../../parsed/duo_105.csv'
# output_file_path = '../../parsed/duo_105_clean.csv'
# clean_text(input_file_path, output_file_path)
# print(pd.read_csv('../../parsed/duo_105_clean.csv').columns)

# input_file_path = '../../parsed/others_4.csv'
# output_file_path = '../../parsed/others_4_clean.csv'
# clean_text(input_file_path, output_file_path)
# print(pd.read_csv('../../parsed/others_4_clean.csv').columns)


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


# if __name__ == '__main__':
#     input_path = '../../uao.csv'
#     utf_8_encoding(input_path)


def citation_del_dups(input_file_folder):
    """
    Delete citation duplicates.
    :param input_file_folder: data folder
    :return: updated csv files
    """

    _, _, filenames = next(os.walk(input_file_folder))
    # print(filenames)
    for c in filenames:
        if c.endswith('csv'):
            df = pd.read_csv(os.path.join(input_file_folder, c))
            df['citations'] = df.citations.apply(lambda x: list(dict.fromkeys(x[1:-1].replace("'", "").split(', '))))
            df.to_csv(os.path.join(input_file_folder, c), index=False)


if __name__ == '__main__':
    input_file_folder = '../data'
    citation_del_dups(input_file_folder)
