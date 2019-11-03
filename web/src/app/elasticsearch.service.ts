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

  fullTextSearch(_queryText) {
    return this.client.search({
      index: "_all",
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
      '_source': ['filename', 'citations', 'circumstance', 'link', 'year']
    });

  }

  simSearch(_queryText) {
    return this.client.search({
      index: "_all",
      body: {
        'query': {
          'more_like_this' : {
            'fields' : ['circumstance'],
            'like' : _queryText,
            "min_term_freq" : 2,
            "max_query_terms" : 50
          }
        }
      },
      '_source': ['filename', 'citations', 'circumstance', 'link', 'year']
    });
  }
}
