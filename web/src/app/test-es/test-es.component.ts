import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ElasticsearchService } from '../elasticsearch.service';
import { FormsModule } from '@angular/forms';
import {BehaviorSubject, Observable, of} from "rxjs";
import {fromPromise} from "rxjs/internal-compatibility";
import {catchError, tap} from "rxjs/operators";

@Component({
  selector: 'app-test-es',
  templateUrl: './test-es.component.html',
  styleUrls: ['./test-es.component.scss']
})

export class TestEsComponent implements OnInit {
  isConnected = false;
  status: string;

  userInput: string;
  response: any;

  // responseSubject: BehaviorSubject<any>;
  // response$: Observable<any>;


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
    // this.response$ = fromPromise(this.es.fullTextSearch(this.userInput)).pipe(
    //   // tap( r => console.log(r)),
    //   catchError(error => of(`Bad Promise: ${error}`))
    // );
    //
    // this.response$.subscribe(
    //   r => console.log(r)
    // );



    // TODO convert promise to Observable
    this.es.fullTextSearch(this.userInput).then(
      response => {
        this.response = response.hits.hits;
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
        console.log(this.response);
      }, error => {
        console.error(error);
      }).then(() => {
      console.log('Search Completed!');
    });
  }

  filter(filterType) {

  }

}
