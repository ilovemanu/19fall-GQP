import {Injectable} from '@angular/core';
import {Client} from 'elasticsearch-browser';
import * as elasticsearch from 'elasticsearch-browser';

@Injectable({
  providedIn: 'root'
})
export class ElasticsearchService {

  private client: Client;

  constructor() {
    if (!this.client) {
      this._connect();
    }
  }

  private _connect() {
    this.client = new elasticsearch.Client({
      host: 'localhost:9200',
      log: 'trace'
    });
  }

  isAvailable(): any {
    return this.client.ping({
      requestTimeout: Infinity,
      body: 'hello alex!'
    });
  }

  fullTextSearch(_queryText, _userYearFilter) {
    if(_userYearFilter === "lastYear"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "match": {
                'circumstance': {
                  'query': _queryText,
                  'operator': 'and'
                }
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-1, "lte" : (new Date()).getFullYear()}
              }
          }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year']
  });
    }
    if(_userYearFilter === "lastFiveYears"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "match": {
                'circumstance': {
                  'query': _queryText,
                  'operator': 'and'
                }
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-5, "lte" : (new Date()).getFullYear()}
              }
          }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
  });
    }
    if(_userYearFilter === "lastTenYears"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "match": {
                'circumstance': {
                  'query': _queryText,
                  'operator': 'and'
                }
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-10, "lte" : (new Date()).getFullYear()}
              }
            }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
  });
    }
    else{
      return this.client.search({
      index: '_all',
      body: {
        'query': {
          'match': {
            'circumstance': {
              'query': _queryText,
              'operator': 'and'
            }
          }
        }
      },
      '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
    });
    }
  }

  simSearch(_queryText, _userYearFilter) {
  console.log(_userYearFilter);
  console.log(_queryText);
  if(_userYearFilter === "lastYear"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "more_like_this": {
                'fields' : ['circumstance'],
                'like' : _queryText,
                "min_term_freq" : 1,
                "max_query_terms" : 50
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-1, "lte" : (new Date()).getFullYear()}
              }
          }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year']
  });
    }
    if(_userYearFilter === "lastFiveYears"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "more_like_this": {
                'fields' : ['circumstance'],
                'like' : _queryText,
                "min_term_freq" : 1,
                "max_query_terms" : 50
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-5, "lte" : (new Date()).getFullYear()}
              }
          }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
  });
    }
    if(_userYearFilter === "lastTenYears"){
      return this.client.search({
       body: {
        "query": {
          "bool": {
            "must": {
              "more_like_this": {
                'fields' : ['circumstance'],
                'like' : _queryText,
                "min_term_freq" : 1,
                "max_query_terms" : 50
              }
            },
            "filter": {
              "range": {
                "year": { "gte" : (new Date()).getFullYear()-10, "lte" : (new Date()).getFullYear()}
              }
          }
         }
        }
       },
    '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
  });
    }
    else{
      return this.client.search({
      index: '_all',
      body: {
        'query': {
          'more_like_this' : {
            'fields' : ['circumstance'],
            'like' : _queryText,
            "min_term_freq" : 1,
            "max_query_terms" : 50
          }
        }
      },
      '_source': ['filename', 'citations', 'circumstance', 'year', 'link']
    });
    }
  }
}
