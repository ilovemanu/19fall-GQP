# Created by alex at 9/27/19
# Parse the 'DESCRIPTION OF NONCOMPLIANCE_2' folder for information.

import os
import re
import csv
import pandas as pd


def test_noncompliance(input_path):
    """
    Find info about the 'description of noncompliance' section
    Group files with multiple noncompliance into temp folder
    :param input_path: input folder path
    :return: all file count, # of files with single noncompliance, # of files with mult noncompliance
    """

    q1 = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'

    counter1 = 0  # track all file
    counter2 = 0  # track file with single noncompliance
    counter3 = 0  # track file with multiple noncompliance
    _, _, filenames = next(os.walk(input_path))
    for file in filenames:
        if file.split('.')[1] == 'txt':
            counter1 += 1
            input_f = os.path.join(input_path, file)
            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                in_file_counter = 0
                for line in f:
                    pattern = re.search(q1, line)
                    if pattern:
                        in_file_counter += 1  # track occurrence
                if in_file_counter > 1:
                    counter3 += 1
                    print(file)
                    # os.rename(input_f, os.path.join(input_path, 'temp', file))  # move to another folder
                else:
                    counter2 += 1
    return counter1, counter2, counter3


# input_path = '../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2'
# print(test_noncompliance(input_path))


def write_csv(csvname, header, data):  # data is a tuple
    """
    Write data to csv.
    :param csvname:
    :param header: a list of field names for header.
    :param data: tuple separated by coma.
    :return:
    """
    with open(csvname, 'a+') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=',')
        # write the header if file is empty
        if csvfile.tell() == 0:
            csvwriter.writerow(i for i in header)
        # writing the data rows
        csvwriter.writerows([data])


def get_citation(q_list, text, req):
    """
    Get citations.
    :param q_list: regex list
    :param text: the description of noncompliance section
    :param req: the description of requirements section, or the whole file
    :return: a list of citations
    """
    citations = []
    # look under 'description of requirements'
    for q in q_list[:-1]:
        citations += re.findall(q, req)
    if len(citations) == 0:
        # look under 'description of noncompliance'
        citations += re.findall(q_list[-1], text)
    return list(set(citations))


def parser(input_path, csvname, header):
    """
    Parse the files with single noncompliance.
    Two scenarios:
    1) 'description of noncompliance' comes before 'description of requirements'
    2) 'description of noncompliance' comes before 'actions to be taken'
    :param input_path: input folder path
    :param csvname: csv filename.
    :param header: csv filename header.
    :return: file counter.
             single (filename w/o extension, list of citations, single noncompliance section) from each file.
    """

    q1 = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'
    q2 = r'DESCRIPTION OF( THE)? RE(QUIREMENT(S)?)?(QUIREMENT\(S\))? NOT(.)? COMPLIED WITH'
    q3 = r'ACTION(S)? TO BE TAKEN'
    q_citation_1 = r'(40[.]\d{4}):'
    q_citation_2 = r'(40[.]\d{4})\(\d\):'
    q_citation_3 = r'(40[.]\d{4})\(\d\) [A-Z]'
    q_citation_4 = r'40\.\d{4}'
    q_list = [q_citation_1, q_citation_2, q_citation_3, q_citation_4]

    counter = 0  # track file #
    _, _, filenames = next(os.walk(input_path))
    for file in filenames:
        input_f = os.path.join(input_path, file)
        with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.readlines()
            citations = []

            for line_num, line in enumerate(data):

                # parse citations * duplicates included
                citations += re.findall(q_citation_1, line)
                citations += re.findall(q_citation_2, line)
                citations += re.findall(q_citation_3, line)

                if re.search(q1, line):
                    n1 = line_num
                elif re.search(q2, line):
                    n2 = line_num
                elif re.search(q3, line):
                    n3 = line_num

            if n2:
                if n1 < n2:  # noncompliance followed by requirements
                    text = ''.join(data[n1:n2])
                    counter += 1
                else:  # noncompliance followed by action
                    text = ''.join(data[n1:n3])
                    counter += 1
            else:  # noncompliance followed by action while requirement missing
                text = ''.join(data[n1:n3])
                counter += 1

            citations = get_citation(q_list, text, ''.join(data))

            # find out filenames with empty citation list
            # add manually
            if len(citations) == 0: print(file)

            # write out data for each file
            # write_csv(csvname, header, (file.split('.')[0], citations, text))

    return counter


# input_path = '../../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2'
# header = ['filename', 'citation list', 'paragraph']
# print(parser(input_path, 'single_293.csv', header))
# 293

def parser_duo(input_path, csvname, header):
    """
    Parse the files with multiple noncompliance.
    Three scenarios:
    1) 'description of noncompliance' comes before 'description of requirements', and their counts match
    2) 'description of noncompliance' comes after 'description of requirements', and their counts match,
        'actions to be taken' at the end.
    3) 'description of noncompliance' count = 'description of requirements' + 'actions to be taken', and
        'description of noncompliance' comes before 'description of requirements', and their counts match
    :param input_path: input folder path.
    :param csvname: csv filename.
    :param header: csv filename header.
    :return: file counter.
             multiple (filename w/o extension, list of citations, single noncompliance section) from each file.
    """
    q1 = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'
    q2 = r'DESCRIPTION OF( THE)? RE(QUIREMENT(S)?)?(QUIREMENT\(S\))?(C YUIREMENTS)? NOT(.)? COMPLIED WITH'
    q3 = r'ACTION(S)?(\(S\))? TO BE TAKEN'
    q_citation_1 = r'(40[.]\d{4}):'
    q_citation_2 = r'(40[.]\d{4})\(\d\):'
    q_citation_3 = r'(40[.]\d{4})\(\d\) [A-Z]'
    q_citation_4 = r'40\.\d{4}'
    q_list = [q_citation_1, q_citation_2, q_citation_3, q_citation_4]

    counter = 0  # track all file
    counter1 = 0  # track files with matching noncompliance and requirement occurrences
    counter2 = 0  # track files with non-matching noncompliance and requirement occurrences
    counter3 = 0  # track all noncompliance occurrences

    _, _, filenames = next(os.walk(input_path))
    for file in filenames:
        if file.split('.')[1] == 'txt':
            input_f = os.path.join(input_path, file)

            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.readlines()
                n1 = []
                n2 = []
                n3 = []

                for line_num, line in enumerate(data):
                    if re.search(q1, line):
                        n1.append(line_num)
                    elif re.search(q2, line):
                        n2.append(line_num)
                    elif re.search(q3, line):
                        n3.append(line_num)

                counter += 1
                if len(n1) == len(n2):
                    counter1 += 1
                    if n1[0] < n2[0]:  # noncompliance comes first
                        if len(n3) == 1:
                            n1.append(n3[0])
                            for i in range(len(n1)-1):
                                counter3 += 1
                                text = ''.join(data[n1[i]:n2[i]])
                                req = ''.join(data[n2[i]:n1[i+1]])
                                citations = get_citation(q_list, text, req)

                                if len(citations) == 0: print(file)
                                # write_csv(csvname, header, (file.split('.')[0], citations, text))

                        else:  # two 'ACTION' sections
                            for i in range(len(n1)):
                                counter3 += 1
                                text = ''.join(data[n1[i]:n2[i]])
                                citations = list(set(re.findall(q_citation_4, text)))
                                if len(citations) == 0: print(file)
                                # write_csv(csvname, header, (file.split('.')[0], citations, text))

                    else:  # requirements comes first, action at the end
                        n2.append(n3[0])
                        for i in range(len(n2)-1):
                            counter3 += 1
                            text = ''.join(data[n1[i]:n2[i+1]])
                            req = ''.join(data[n2[i]:n1[i]])
                            citations = get_citation(q_list, text, req)

                            if len(citations) == 0: print(file)
                            # write_csv(csvname, header, (file.split('.')[0], citations, text))
                else:  # len(n2) < len(n1) and 'noncompliance' comes first
                    counter2 += 1
                    n2.append(n3[0])
                    for i in range(len(n1)):
                        counter3 += 1
                        text = ''.join(data[n1[i]:n2[i]])
                        citations = list(set(re.findall(q_citation_4, text)))
                        if len(citations) == 0: print(file)
                        # write_csv(csvname, header, (file.split('.')[0], citations, text))

    return counter, counter1, counter2, counter3


# input_path = '../../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2/temp'
# header = ['filename', 'citation list', 'paragraph']
# print(parser_duo(input_path, 'duo_105.csv', header))
# (104, 101, 3, 235)


def count_row(file_path):
    """
    Get number of rows/records in a csv file.
    :param file_path: csv file path
    :return: number of rows in the csv file
    """
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        count = sum(1 for line in reader)
    return count


# file_path = 'out_alex_duo.csv'
# print((count_row(file_path)))


def others_parser(csv_path):
    """
    Update data csv with citations from copy & pasted paragraphs.
    :param csv_path:
    :return: updated csv
    """
    q_citation_1 = r'40.\d{4}'
    q_citation_2 = r'40,\d{4}'

    df = pd.read_csv(csv_path)
    # print(df.columns)  # ['filename', 'citations', 'paragraph']

    citations = []
    null_idx = df[df.citations.isnull()].index.tolist()
    tmp = df[df.citations.isnull()].paragraph.tolist()

    for i, t in enumerate(tmp):
        c = []
        c += re.findall(q_citation_1, t)
        c += re.findall(q_citation_2, t)
        citations.append(list(set(c)))

    df.citations.iloc[null_idx] = citations
    df.to_csv('../../others_4.csv', index=False)


# others_parser('../../others_4 copy.csv')


def acop_parser(input_path, csv_path):

    q1 = r'STATEMENT OF( ALLEGED)? FACTS AND LAW'
    q2 = r'DISPOSITION AND ORDER'
    q3 = r'Consented To:'
    q4 = r'SUPPLEMENTAL ENVIRONMENTAL PROJECT SUMMARY'
    qc = r'40[.,]\d{4}'

    counter = 0  # track file num

    _, _, filenames = next(os.walk(input_path))

    for file in filenames:
        if file.endswith('.txt'):
            input_f = os.path.join(input_path, file)

            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                counter += 1
                data = f.readlines()

                for line_num, line in enumerate(data):
                    if re.search(q1, line):
                        n1 = line_num
                    elif re.search(q2, line):
                        n2 = line_num
                    elif re.search(q3, line):
                        n3 = line_num
                    elif re.search(q4, line):
                        n4 = line_num

                if n1 > n2: print(file)

                facts_and_law = ''.join(data[n1+1:n2])
                citations = re.findall(qc, facts_and_law)
                for c in citations:
                    if c[2] == ',': c.replace(',', '.')
                    if ' ' in c: c.replace(' ', '')
                    if c == '40.0000':
                        citations.remove(c)
                    if c[2] == ',': c.replace(',', '.')

                if len(citations) == 0: print('missing citations: ', file)

                # write out data for each file
                header = ['filename', 'citations', 'circumstance']
                write_csv(csv_path, header, (file.split('.')[0], list(set(citations)), facts_and_law))
    print('Done!')
    return counter


# if __name__ == '__main__':
#     input_path = '../../ACOPs_txt'
#     csv_path = '../../ACOPs.csv'
#     acop_parser(input_path, csv_path)


def uao_parser(input_path, csv_path):

    q1 = r'STATEMENT OF FACTS AND LAW'
    q2 = r'DISPOSITION( AND ORDER)?'
    qc = r'40[.,]\d{4}'

    counter = 0  # track file num

    _, _, filenames = next(os.walk(input_path))

    for file in filenames:
        if file.endswith('.txt'):
            input_f = os.path.join(input_path, file)

            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                counter += 1
                data = f.readlines()
                counter_1 = 0
                counter_2 = 0

                for line_num, line in enumerate(data):

                    if re.search(q1, line):
                        n1 = line_num
                        counter_1 += 1
                    elif re.search(q2, line):
                        n2 = line_num
                        counter_2 += 1

                if n1 > n2: print(file)

                facts_and_law = ''.join(data[n1+1:n2])
                citations = re.findall(qc, facts_and_law)
                for c in citations:
                    if c[2] == ',': c.replace(',', '.')
                    if ' ' in c: c.replace(' ', '')
                    if c == '40.0000':
                        citations.remove(c)
                    if c[2] == ',': c.replace(',', '.')

                if len(citations) == 0: print('missing citations: ', file)

                # write out data for each file
                header = ['filename', 'citations', 'circumstance']
                write_csv(csv_path, header, (file.split('.')[0], list(set(citations)), facts_and_law))
    print('Done!')
    return counter


# if __name__ == '__main__':
#     input_path = '../../UAOs_txt'
#     csv_path = '../../uao.csv'
#     uao_parser(input_path, csv_path)



def achu_part(input_path1, input_path2):

    raw2 = pd.read_csv(input_path2)
    raw2 = raw2[raw2.filename.notnull()]
    raw1 = pd.read_csv(input_path1)
    raw1 = raw1[raw1.filename.notnull()]

    combine = pd.concat([raw1, raw2])
    combine.to_csv('../../achu_combine.csv', index=False)

    print(combine[combine.citations == '[]']['filename'])





