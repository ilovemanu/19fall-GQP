# Created by alex at 10/25/19


from PyPDF2 import PdfFileReader
import os


def pdf_page_checker(pdf_folder_path, txt_folder_path, output_path):
    """
    Check number_of_pages of each pdf file.
    If number_of_pages is less than a threshold,
    ignore the file by moving to a separate folder.
    :param pdf_folder_path: pdf file folder
    :param txt_folder_path: txt file folder
    :param output_path: the separate folder
    :return:
    """

    counter = 0
    _, _, filenames = next(os.walk(pdf_folder_path))

    for file in filenames:
        print(file)
        if file.endswith('.pdf') or file.endswith('.PDF'):
            input_f = os.path.join(pdf_folder_path, file)
            with open(input_f, 'rb') as f:
                pdf = PdfFileReader(f)
                number_of_pages = pdf.getNumPages()

            print(number_of_pages)
            if number_of_pages <= 3:
                txt_name = file.split('.')[0]+'.txt'
                txt_file_path = os.path.join(txt_folder_path, txt_name)
                os.rename(txt_file_path, os.path.join(output_path, txt_name))
                counter += 1

    print(counter)


if __name__ == '__main__':
    pdf_folder_path = '../../UAOs'
    txt_folder_path = '../../UAOs_txt'
    output_path = '../..//UAOs_waste'
    pdf_page_checker(pdf_folder_path, txt_folder_path, output_path)
