import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ElasticsearchService } from '../elasticsearch.service';
import { FormsModule } from '@angular/forms';
import {Observable} from "rxjs";
import {and} from "@angular/router/src/utils/collection";

@Component({
  selector: 'app-test-es',
  templateUrl: './test-es.component.html',
  styleUrls: ['./test-es.component.scss']
})

export class TestEsComponent implements OnInit {
  isConnected = false;
  status: string;

  userInput: string;
  userYearFilter = 'allTime';
  userTypeFilter = '_all';
  response: any[];
  filteredResponse: any[];


  constructor(private es: ElasticsearchService, private cd: ChangeDetectorRef) {
    this.isConnected = false;
  }

  ngOnInit() {
    this.es.isAvailable().then(() => {
      this.status = 'OK';
      this.isConnected = true;
    }, error => {
      this.status = 'ERROR';
      this.isConnected = false;
      console.error('Server is down', error);
    }).then(() => {
      this.cd.detectChanges();
    });

  }

  exactMatch() {
    // TODO convert promise to Observable
    console.log(this.userInput);
    console.log(this.userYearFilter);
    this.es.fullTextSearch(this.userInput).then(
      response => {
        this.response = response.hits.hits;
        this.filteredResponse = this.response;
        console.log(this.response);
      }, error => {
        console.error(error);
      }).then(() => {
      console.log('Search Completed!');
    });
  }

  simSearch() {
    this.es.simSearch(this.userInput).then(
      response => {
        this.response = response.hits.hits;
        this.filteredResponse = this.response;
        console.log(this.response);
      }, error => {
        console.error(error);
      }).then(() => {
      console.log('Search Completed!');
    });
  }

  // TODO: chaining the two filters
  typeFilterChanged(type: string) {
    console.log(type);

    if ( type === '_all') {
      this.filteredResponse = this.response;
    } else {
      this.filteredResponse = this.response.filter(doc => doc._index === type);
    }
  }

  yearFilterChanged(year: string) {
    console.log(year)


    if ( year === 'allTime') {
      this.filteredResponse = this.response;
    }
    else if ( year === 'lastYear') {
      this.filteredResponse = this.response.filter(doc => {
        console.log(`+doc._source.year: ${+doc._source.year}`);
        console.log(`new Date().getFullYear() - 1: ${new Date().getFullYear() - 1}`);

        return +doc._source.year > new Date().getFullYear() - 1
      });
    }
    else if ( year === 'lastFiveYears') {
      this.filteredResponse = this.response.filter(
        doc => +doc._source.year > new Date().getFullYear() - 5
      );
    }
    else if ( year === 'lastTenYears') {
      this.filteredResponse = this.response.filter(
        doc => +doc._source.year > new Date().getFullYear() - 10
      );
    }
  }
}
