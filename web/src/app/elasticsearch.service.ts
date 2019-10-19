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
      index: 'test',
      body: {
        'query': {
          'match': {
            'clean': {
              'query': _queryText,
              'operator': 'and'
            }
          }
        }
      },
      '_source': ['filename', 'citations', 'clean']
    });

  }

  simSearch(_queryText) {
    return this.client.search({
      index: 'test',
      body: {
        'query': {
          'more_like_this' : {
            'fields' : ['clean'],
            'like' : _queryText
          }
        }
      },
      '_source': ['filename', 'citations', 'clean']
    });
  }
}
