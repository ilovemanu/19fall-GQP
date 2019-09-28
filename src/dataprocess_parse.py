import glob
import csv
import os
import re


def parse_each_file(file):
    """Parse each files to get the useful info, filename, citationlist, circumstance
        Parameters
        ----------
        folder_path : str
            String representation of the folder path containing the text files.

        Outputs
        name:str
         file name, use this for unique id
        citation_lists:list
         list of the citations
        circumstance_result: str
         the whole paragraph of description in the file

        """

    useful_titles = ['DESCRIPTION OF NONCOMPLIANCE:', 'DESCRIPTION OF ACTIVITY OR OMISSION CONSTITUTING NONCOMPLIANCE:',
                     'DESCRIPTION OF ACTIVITY (OR OMISSION) IN NONCOMPLIANCE:',
                     'DESCRIPTION OF ACTIVITY CONSTITUTING NONCOMPLIANCE:',
                     'DESCRIPTION OF ACTIVITY NONCOMPLIANCE:']

    with open(file, 'rt', encoding="utf8") as f:
        # Name Processing
        name = os.path.basename(f.name).strip(".txt")
        lines = f.readlines()
        # citation
        citation_list = []
        for line in lines:
            if "310" in line:
                citation_star = line.find('310')
                citation_fin = citation_star + 15
                citation_name = line[citation_star:citation_fin]
                citation_list.append(citation_name)
        citation_lists = list(set(citation_list))  # citation_result is a list
        # circumstance
        cicumstance_list = []
        title_line = []
        for line in lines:
            for title in useful_titles:
                if title in line:
                    title_line.append(lines.index(line))
                    break
        title_line = list(set(title_line))
        # for i in range(len(title_line)) :
        # print(lines[title_line[i]])
        for i in range(len(title_line)):
            cicums_star = title_line[i]
            for j in range(cicums_star + 1, len(lines), 1):
                line_info = lines[j]
                no_num = 0
                for i in range(len(line_info)):
                    if line_info[i].isupper() == False:
                        no_num = no_num + 1
                if 2 < no_num <= 10:
                    # print("The Circumstance is ")
                    # cicums_stops = j
                    break

                for l in range(cicums_star, j):  # slice the result list
                    cicumstance_list.append(lines[l])
        cir = "".join(cicumstance_list)  # list to string
        strinfo = re.compile(' ')
        circumstance_result = strinfo.sub('', cir)
        # print("The Circumstance is ",circumstance_result)
        # print("The Citation is ",citation_lists)
        # write_csv(csvname, (file.split('.')[0], circumstance_result))

    return name, citation_lists, circumstance_result


def produce_csv(input_path, csvname):
    """Produces a csv of file name, citations and descriptions of a folder with text files
    Parameters
    ----------
    input_path : str
        String representation of the folder path containing the text files.
    csvname : str
        Name of the output file the merged lines will be written to.
    """

    # get all text files
    txt_files = glob.glob(input_path + "*.txt")

    # write to file
    writer = csv.writer(open(input_path + csvname, "wt"))
    headers = ['file name', 'citation', 'description']
    writer.writerow(headers)

    for f in txt_files:
        result_ = parse_each_file(f)
        writer.writerow(result_)


