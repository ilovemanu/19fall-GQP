# Created by alex at 9/21/19

import os
import re


def clean_ext(input_path):
    """
    Clean out files with ext tag in the file name.
    :param input_path: folder to be cleaned.
    :return:
    """
    pattern = r" ext.?(ention)?"
    counter = 0
    for _, _, filenames in os.walk(input_path):
        for f in filenames:
            target = re.search(pattern, f, re.IGNORECASE)
            if target:
                counter += 1
                print(f)
                os.remove(os.path.join(input_path, f))

    return counter

# print(clean_ext('../NONs_txt'))
# ~179

def collect_CI(input_path, output_folder_name):
    """
    Collect all files with 'CI' in the filename into one folder.
    :param input_path: path of the input folder
    :return: collected files within one folder
    """

    output_path = os.path.join(input_path, output_folder_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    pattern = r' CI '
    counter = 0

    _, _, filenames = next(os.walk(input_path))
    for f in filenames:
        target = re.search(pattern, f, re.IGNORECASE)
        if target:
            counter += 1
            print(f)
            os.rename(os.path.join(input_path, f), os.path.join(output_path, f))

    return counter

# print(collect_CI('../NONs_txt_2600', 'CI'))
