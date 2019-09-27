# Created by alex at 9/21/19

import os
import re


def split(input_path, target, re_target):
    """
    Split files into sub-folders based on string target.
    :param input_path: input folder path
    :param target: target string
    :param re_target: regex string to be targeted
    :return:
    """

    # create a sub-folder using format a the name
    output_folder = os.path.join(input_path, target)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    counter = 0
    _, _, filenames = next(os.walk(input_path))

    for file in filenames:
        input_f = os.path.join(input_path, file)
        # print(input_f)
        with open(input_f, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                pattern = re.search(re_target, line)
                if pattern:
                    print(file)
                    counter += 1
                    os.rename(input_f, os.path.join(output_folder, file))
                    break
    return counter


# target = 'DESCRIPTION OF NONCOMPLIANCE'
# re_target = r'DESCRIPTION(S)? OF NON(COMPLIANCE)?'

# target = 'DESCRIPTION OF ACTIVITY OR OMISSION CONSTITUTING NONCOMPLIANCE'
# re_target = r'DESCRIPTION OF ACT(IVITY)?(IVITIES)? OR OMISSION CONSTITUTING'

# target = 'DESCRIPTION OF ACTIVITY IN NONCOMPLIANCE'
# re_target = r'DESCRIPTION(S)? OF ACTIVIT(Y)?(IES)?( OR OMISSION)? IN'

# target = 'DESCRIPTION OF ACTIVITY NONCOMPLIANCE'
# re_target = r'DESCRIPTION OF ACTIVITY NONCOMPLIANCE'

# target = 'DESCRIPTION OF ACTIVITY CONSTITUTING NONCOMPLIANCE'
# re_target = r'DESCRIPTION OF ACTIVITY CON(STITUTING NONCOMPLIANCE)?'

# split('../NONs_txt_2600', target, re_target)


def split_further(input_folder, output_folder):

    """
    Further split files for workload distribution.
    :param input_folder: input folder path.
    :param output_folder: output_folder name.
    :return: files split into different folders.
    """
    counter = 0
    _, _, filenames = next(os.walk(input_folder))

    for file in filenames:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)
        os.rename(input_path, output_path)
        counter += 1
        if counter == 175: break

    return counter


print(split_further('../NONs_txt_2600/others_1', '../NONs_txt_2600/others_4'))