# Created by alex at 11/2/19

import pandas as pd


def add_link(csv_path):

    df = pd.read_csv(csv_path)
    df['link'] = "https://eeaonline.eea.state.ma.us/EEA/fileviewer/Rtn.aspx?rtn=" + df['RTNs'].astype(str)
    # print(df.link[0])
    df.to_csv(csv_path, index=False)


if __name__ == '__main__':
    csv_path = ['../../non.csv', '../../acop.csv', '../../uao.csv']
    for c in csv_path:
        add_link(c)
        print(pd.read_csv(c)['link'][0])
