"""
Created on Thu Sep 15 06:36:47 2019

@author: alex
"""

import os
import re


def get_unique_id(folder_path):
    """
    Count unique doc IDs.
    input_path is the path of the input folder.
    Output is the # of unique doc ids.
    """

    # folder_path = '../NONs_txt'
    ids = []
    for _, _, filenames in os.walk(folder_path):
        for f in filenames:

            # print(f.split(' - ')[0])
            id = f.split(' - ')[0]
            if id not in ids:
                ids.append(id)
    return len(ids)


# print(get_unique_id('../NONs_txt'))
# 1586 unique doc ids


def count_audit(input_path):
    """
    Count approx. number of audit files
    :param input_path: input folder path
    :return: file number
    """
    pattern = r'N(O)?AF(NON)?' # NOAF NAFNON NOAFNON others
    counter = 0
    for _, _, filenames in os.walk(input_path):
        for f in filenames:
            target = re.search(pattern, f, re.IGNORECASE)
            if target:
                print(f)
                counter += 1
    return counter


# print(count_audit('../NONs_txt_2600 copy 5'))
# ~914


def get_doc_number(folder_path):
    """
    Count unique doc IDs.
    input_path is the path of the input folder.
    Output is the # of unique doc ids.
    """

    # folder_path = '../NONs_txt_2600'
    # target = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'
    # target = r'DESCRIPTION OF ACT(IVITY)?(IVITIES)? OR OMISSION CONSTITUTING'
    # target = r'DESCRIPTION(S)? OF ACTIVIT(Y)?(IES)?( OR OMISSION)? IN'
    # target = r'DESCRIPTION OF ACTIVITY CON(STITUTING NONCOMPLIANCE)?'
    # target = r'DESCRIPTION OF ACTIVITY NONCOMPLIANCE'

    counter = 0
    for _, _, filenames in os.walk(folder_path):
        for file in filenames:
            input_f = os.path.join(folder_path, file)
            # print(input_f)
            with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    reg_target = re.search(target, line)
                    # reg_target2 = re.search(target2, line)
                    if reg_target:# and not reg_target2:
                        print(file)
                        counter += 1
                        # file or occurrence
                        break

    return counter

# print(get_doc_number('../NONs_txt_2600 copy 5'))
