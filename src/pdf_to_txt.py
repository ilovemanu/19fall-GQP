#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:43:47 2019

@author: alex
"""

import os 
from pdf2image import convert_from_path 
import pytesseract
from PIL import Image


def pdf_to_txt(pdf_file, output_folder):
    
    """
    Convert scanned pdf to jpg by pdf2image.
    Convert jpg to txt by pytesseract.
    pdf_file is the file PATH with .pdf extension as string.
    output_folder is folder name for the txt file.
    """
    
    # create output folder 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # pdf to jpg
    pages = convert_from_path(pdf_file, dpi=300) # dpi adjustable
    image_counter = 1

    for page in pages:
    
        filename = 'page_' + str(image_counter)+ '.jpg'
        page.save(filename, 'JPEG')
        image_counter += 1
    
    # extract file name from path w/o extension
    outfile = os.path.split(pdf_file)[1].split('.')[0]+'.txt'
    
    # out path
    out = os.path.join(output_folder, outfile)
    
    # jpg to txt
    print('creating pdf: ' + out)
    f = open(out, 'a+')
    
    filelimit = image_counter - 1
    
    for i in range(1, filelimit+1):
        filename = 'page_'+str(i)+'.jpg'
        
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = text.replace('-\n', '')     
        f.write(text)
        
        # remove the jpg file to save space
        os.remove(filename)

    f.close()

 
# test
#pdf_to_txt('2-0000003 - ACTON - L3 NAFNON with sketch plan 03-14-2014.pdf', 'NON_txt')
