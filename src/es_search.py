# Created by alex at 10/6/19


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
                "analyzer": "english",  # will deal with stopwords
                "term_vector": "yes",
                "similarity": "BM25"
            }
        }
    }
}


def csv_reader(file_name, index_name):
    """
    Bulk load a csv file into Elasticsearch.
    :param file_name: input file path
    :return:
    """
    # delete index if exists
    es.indices.delete(index=index_name, ignore=[400, 404])
    # create index, set mapping
    es.indices.create(index=index_name, body=mapping)

    with open(file_name, 'r') as outfile:
        reader = csv.DictReader(outfile)
        helpers.bulk(es, reader, index=index_name)

    print("Done!")


if __name__ == '__main__':
    input_folder_path = '../../all_csv'
    csv_reader('../../all_csv/NONs.csv', 'non')



# test
# res = es.search(index="test", body={"query": {"match_all": {}}})
# pprint.pprint(res['hits']['hits'])
#
# query = {"match": {"citations": "['40.0311']"}}
# res = es.search(index="test", body={"query": query})
# pprint.pprint(len(res['hits']['hits']))
# pprint.pprint(len(res['hits']['hits']))
#
# query = {"match": {"clean": "groundwater"}}
# res = es.search(index="test", body={"query": query})
# pprint.pprint(res['hits']['hits'])
# pprint.pprint(len(res['hits']['hits']))
