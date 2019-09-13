#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 16:17:02 2019

@author: alex
"""

import pdf_to_txt
import os 

def batch_pdf_to_txt(input_folder, output_folder):
    
    """
    Convert pdf to txt in batch.
    input_folder is the pdf folder name.
    output_folder is the txt folder name.
    
    """
    
    
    for dirpath, dirnames, filenames in os.walk(input_folder):
#        print(dirpath)
#        print(dirnames)
#        print(filenames)
        
        for f in filenames:
            # error control -> macos folders have .DS_Store file.
            if f.endswith('.pdf') or f.endswith('.PDF'):
                input_f = os.path.join(input_folder, f)
                try:
                    pdf_to_txt.pdf_to_txt(input_f, output_folder)
                except:
                    continue
            
     
# batch convert
#batch_pdf_to_txt('NONs', 'NONs_txt')
