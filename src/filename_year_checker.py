# Created by alex at 10/25/19

import os

ok_list = ['2-0015666 - Hudson - ACOP.txt',
           '2-0015564 - Acton - ACOP-2.txt',
           '2-0018831 - Charlton - ACOP Final for Sig.txt',
           '2-0018127 - LEOMINSTER - ACOP 03-06-213.txt',
           '2-0019101-Holden-Draft ACOP-CE-15-3R002-NT.txt']


def filename_year_checker(input_folder, output_folder):

    _, _, filenames = next(os.walk(input_folder))

    for file in filenames:
        if file.endswith('.txt'):
            title = file.split('.')[0]
            year = title.split(' ')[-1].split('-')[-1]
            if file not in ok_list and int(year) < 2000:
                print(file)
                # os.rename(os.path.join(input_folder, file), os.path.join(output_folder, file))
            # break



if __name__ == '__main__':
    input_folder = '../../ACOPs_txt'
    output_folder = '../../ACOPs_waste'
    filename_year_checker(input_folder, output_folder)
