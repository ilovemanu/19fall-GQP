import glob
import csv
import os
import re


def read_first_line(file):
    """Gets the name of the file and the citations specified in the file

    Returns
    -------
    str
        Returns a comma-delimited format of the file name and list of citations
    """
    listOfCitations = ""
    citationsList = [];

    with open(file, 'rt', encoding="utf8") as fd:
        name = os.path.basename(fd.name).strip(".txt")
        matches = re.findall(r'310 CMR 40.\d\d\d\d', fd.read());
        for m in matches:
            citationsList.append(m.replace(",", "."))
        uniqueCitations = set(citationsList)
        first = True
        for uc in uniqueCitations:
            if first:
                first = False
                listOfCitations = uc
            else:
                listOfCitations = listOfCitations + " / " + uc

    return name,listOfCitations,""

def merge_per_folder(folder_path, output_filename):
    """Merges first lines of text files in one folder, and
    writes combined lines into new output file

    Parameters
    ----------
    folder_path : str
        String representation of the folder path containing the text files.
    output_filename : str
        Name of the output file the merged lines will be written to.
    """
    # make sure there's a slash to the folder path
    folder_path += "" if folder_path[-1] == "/" else "/"
    # get all text files
    txt_files = glob.glob(folder_path + "*.txt")

    # write to file
    csvex = csv.writer(open(folder_path + output_filename, "wt"))
    headers = ['file name', 'description', 'citation']
    csvex.writerow(headers)

    for f in txt_files:
        s = read_first_line(f)
        print(s)
        csvex.writerow(s)

merge_per_folder(r"C:\Users\Achu\PycharmProjects\NONs_txt_split\NONs_txt_split\DESCRIPTION OF ACTIVITY OR OMISSION CONSTITUTING NONCOMPLIANCE", r"\output")
