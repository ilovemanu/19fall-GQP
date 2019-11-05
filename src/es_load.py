# Created by alex at 10/6/19

import os
import csv
from elasticsearch import helpers, Elasticsearch
import pprint

# Connect...
# Do not need portal information if connected through terminal.
es = Elasticsearch()
mapping = {
    "mappings": {
        "properties": {
            "filename": {
                "type": "text"
            },
            "citations": {
                "type": "text"
            },
            "circumstance": {
                "type": "text",
                "analyzer": "english",  # Deal with stopwords
                "term_vector": "yes",  # Save term vectors at indexing
                "similarity": "BM25"  # TF/IDF-based similarity
            },
            "year": {
                "type": "integer"
            },
            "link": {
                "type": "text"
            }
        }
    }
}


def csv_reader(input_folder_path):
    """
    Bulk load a csv file into Elasticsearch.
    :param input_folder_path: input folder contains multiple csv files
    :return:
    """

    _, _, filenames = next(os.walk(input_folder_path))

    for file in filenames:
        if file.endswith('.csv'):
            data_type = file.split('.')[0]

            # delete index if exists
            es.indices.delete(index=data_type, ignore=[400, 404])
            # create index, set mapping
            es.indices.create(index=data_type, body=mapping)

            with open(os.path.join(input_folder_path, file), 'r') as outfile:
                reader = csv.DictReader(outfile)
                helpers.bulk(es, reader, index=data_type)

    print("Done!")


if __name__ == '__main__':
    input_folder_path = '../data'
    csv_reader(input_folder_path)


# test

# res = es.search(index="non", body={"query": {"match_all": {}}})
# pprint.pprint(res['hits']['hits'])
#
# query = {"match": {"citations": "['40.0311']"}}
# res = es.search(index="non", body={"query": query})
# pprint.pprint(len(res['hits']['hits']))
# pprint.pprint(len(res['hits']['hits']))
#
# query = {"match": {"clean": "groundwater"}}
# res = es.search(index="non", body={"query": query})
# pprint.pprint(res['hits']['hits'])
# pprint.pprint(len(res['hits']['hits']))
