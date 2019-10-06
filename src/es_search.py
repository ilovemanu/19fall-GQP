# Created by alex at 10/6/19


import csv
from elasticsearch import helpers, Elasticsearch
import pprint

# Connect...
# Do not need portal information if connected through terminal.
es = Elasticsearch()


def csv_reader(file_name):
    """
    Load a csv file into Elasticsearch.
    :param file_name: input file path
    :return:
    """
    with open(file_name, 'r') as outfile:
        reader = csv.DictReader(outfile)
        helpers.bulk(es, reader, index="test", doc_type="document")


# csv_reader('test.csv')

# test
res = es.search(index="test", body={"query": {"match_all": {}}})
pprint.pprint(res['hits']['hits'])

query = {"match": {"citations": "['40.0311']"}}
res = es.search(index="test", body={"query": query})
pprint.pprint(len(res['hits']['hits']))
pprint.pprint(len(res['hits']['hits']))

query = {"match": {"clean": "groundwater"}}
res = es.search(index="test", body={"query": query})
pprint.pprint(res['hits']['hits'])
pprint.pprint(len(res['hits']['hits']))
