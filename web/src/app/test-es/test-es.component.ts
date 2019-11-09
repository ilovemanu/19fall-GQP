import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ElasticsearchService } from '../elasticsearch.service';


@Component({
  selector: 'app-test-es',
  templateUrl: './test-es.component.html',
  styleUrls: ['./test-es.component.scss']
})

export class TestEsComponent implements OnInit {
  readonly DEFAULT_YEAR_FILTER = 'allTime';
  readonly DEFAULT_TYPE_FILTER = '_all';

  isConnected = false;
  status: string;

  userInput: string;
  userYearFilter = this.DEFAULT_YEAR_FILTER;
  userTypeFilter = this.DEFAULT_TYPE_FILTER;
  response: any[];
  filteredResponse: any[];
  filteredTypeResponse: any[];
  filteredYearResponse: any[];


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

    this.userYearFilter = this.DEFAULT_YEAR_FILTER;
    this.userTypeFilter = this.DEFAULT_TYPE_FILTER;
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

    this.userYearFilter = this.DEFAULT_YEAR_FILTER;
    this.userTypeFilter = this.DEFAULT_TYPE_FILTER;
  }

  // TODO: chaining the two filters
  typeFilterChanged(type: string) {
    console.log(type);

    if ( type === '_all') {
      this.filteredTypeResponse = this.response;
    } else {
      this.filteredTypeResponse = this.response.filter(doc => doc._index === type);
    }
      this.filteredResponse = this.filteredYearResponse ? this.filteredTypeResponse.filter(type => this.filteredYearResponse.includes(type)) : this.filteredTypeResponse;
  }

  yearFilterChanged(year: string) {
    console.log(year)

    if ( year === 'allTime') {
      this.filteredYearResponse = this.response;
    }
    else if ( year === 'lastYear') {
      this.filteredYearResponse = this.response.filter(doc => {
        console.log(`+doc._source.year: ${+doc._source.year}`);
        console.log(`new Date().getFullYear() - 1: ${new Date().getFullYear() - 1}`);

        return +doc._source.year > new Date().getFullYear() - 1
      });
    }
    else if ( year === 'lastFiveYears') {
      this.filteredYearResponse = this.response.filter(
        doc => +doc._source.year > new Date().getFullYear() - 5
      );
    }
    else if ( year === 'lastTenYears') {
      this.filteredYearResponse = this.response.filter(
        doc => +doc._source.year > new Date().getFullYear() - 10
      );
    }

    this.filteredResponse = this.filteredTypeResponse ? this.filteredYearResponse.filter(year => this.filteredTypeResponse.includes(year)) : this.filteredYearResponse;
    console.log(this.filteredResponse);
  }
}
