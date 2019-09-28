# Created by alex at 9/27/19
# Parse the 'DESCRIPTION OF NONCOMPLIANCE_2' folder for information.

import os
import re
import csv


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


# (398, 293, 105)  # found two more no_info files

# def test_requirement(input_path):
#     """
#     Find info about the 'Description of requirements not complied with' section
#     :param input_path:
#     :return:
#     """
#
#     q2 = r'DESCRIPTION OF( THE)? RE(QUIREMENT(S)?)?(QUIREMENT\(S\))? NOT(.)? COMPLIED WITH'
#     # q3 = r'ACTION(\(S\))?(S)?(s)? TO BE TAKEN'
#
#     counter = 0
#     _, _, filenames = next(os.walk(input_path))
#     for file in filenames:
#         input_f = os.path.join(input_path, file)
#         with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
#             in_file_counter = 0
#             for line in f:
#                 pattern = re.search(q2, line)
#                 # pattern = re.search(q3, line)
#                 if pattern:
#                     in_file_counter += 1
#
#         if in_file_counter == 1: counter += in_file_counter
#         elif in_file_counter == 0:
#             print(file)
#             # os.rename(input_f, os.path.join(input_path, 'temp2', file))  # move to another folder
#         else:
#             print('more', file)
#             # os.rename(input_f, os.path.join(input_path, 'temp2', file))  # move to another folder
#
#     return counter


# input_path = '../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2'
# print(test_requirement(input_path))


def write_csv(csvname, data):  # data is a tuple
    """
    Append data (tuple) to csv.
    :param csvname: csv file name
    :param data: a tuple representing a row, separated by comma.
    :return:
    """
    with open(csvname, 'a+') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=',')
        # writing the data rows
        csvwriter.writerows([data])


# TO-DO: parse citations.
def parser(input_path, csvname):
    """
    Parse the files with single noncompliance.
    Two scenarios:
    1) 'description of noncompliance' comes before 'description of requirements'
    2) 'description of noncompliance' comes before 'actions to be taken'
    :param input_path: input folder path
    :param csvname: csv filename.
    :return: file counter.
             single (filename w/o extension, single noncompliance section) from each file.
    """

    q1 = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'
    q2 = r'DESCRIPTION OF( THE)? RE(QUIREMENT(S)?)?(QUIREMENT\(S\))? NOT(.)? COMPLIED WITH'
    q3 = r'ACTION(S)? TO BE TAKEN'

    counter = 0
    _, _, filenames = next(os.walk(input_path))
    for file in filenames:
        input_f = os.path.join(input_path, file)
        with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.readlines()
            for line_num, line in enumerate(data):
                if re.search(q1, line):
                    n1 = line_num
                elif re.search(q2, line):
                    n2 = line_num
                elif re.search(q3, line):
                    n3 = line_num

            if n2:
                if n1 < n2:  # noncompliance followed by requirements
                    text = ''.join(data[n1:n2])
                    # print(file)
                    # print(text)
                    counter += 1
                    write_csv(csvname, (file.split('.')[0], text))
                else:  # noncompliance followed by action
                    text = ''.join(data[n1:n3])
                    # print(file)
                    # print(text)
                    counter += 1
                    write_csv(csvname, (file.split('.')[0], text))
            else:  # noncompliance followed by action while requirement missing
                text = ''.join(data[n1:n3])
                # print(file)
                # print(text)
                counter += 1
                write_csv(csvname, (file.split('.')[0], text))

    return counter


# input_path = '../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2'
# print(parser(input_path, 'out_alex.csv'))
# 293

def parser_duo(input_path, csvname):
    """
    Parse the files with multiple noncompliance.
    Three scenarios:
    1) 'description of noncompliance' comes before 'description of requirements', and their counts match
    2) 'description of noncompliance' comes after 'description of requirements', and their counts match,
        'actions to be taken' at the end.
    3) 'description of noncompliance' count = 'description of requirements' + 'actions to be taken', and
        'description of noncompliance' comes before 'description of requirements', and their counts match
    :param input_path: input folder path
    :param csvname: csv filename
    :return: file counter.
             multiple (filename w/o extension, single noncompliance section) from each file.
    """

    q1 = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'
    q2 = r'DESCRIPTION OF( THE)? RE(QUIREMENT(S)?)?(QUIREMENT\(S\))?(C YUIREMENTS)? NOT(.)? COMPLIED WITH'
    q3 = r'ACTION(S)?(\(S\))? TO BE TAKEN'

    counter = 0  # track all file
    counter1 = 0  # track files with matching noncompliance and requirement occurrences
    counter2 = 0  # track files with non-matching noncompliance and requirement occurrences
    counter3 = 0  # track all noncompliance occurrences
    _, _, filenames = next(os.walk(input_path))
    for file in filenames:
        if file.split('.')[1] == 'txt':
            input_f = os.path.join(input_path, file)
            n1 = []
            n2 = []
            n3 = []
            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.readlines()
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
                    for i in range(len(n1)):
                        counter3 += 1
                        text = data[n1[i]:n2[i]]
                        write_csv(csvname, (file.split('.')[0], text))

                else:  # requirements comes first, action at the end
                    # print(file, n3)
                    n2.pop(0)
                    n2.append(n3[0])
                    for i in range(len(n1)):
                        counter3 += 1
                        text = data[n1[i]:n2[i]]
                        write_csv(csvname, (file.split('.')[0], text))
            else:
                counter2 += 1
                n2.append(n3[0])
                for i in range(len(n1)):
                    counter3 += 1
                    text = data[n1[i]:n2[i]]
                    write_csv(csvname, (file.split('.')[0], text))

    return counter, counter1, counter2, counter3


# input_path = '../NONs_txt_split/DESCRIPTION OF NONCOMPLIANCE_2/temp'
# print(parser_duo(input_path, 'out_alex_duo.csv'))
# (105, 102, 3, 239)

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
