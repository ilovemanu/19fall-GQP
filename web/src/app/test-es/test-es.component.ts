import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ElasticsearchService } from '../elasticsearch.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-test-es',
  templateUrl: './test-es.component.html',
  styleUrls: ['./test-es.component.css']
})

export class TestEsComponent implements OnInit {
  isConnected = false;
  status: string;

  userInput: string;
  response: any;


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

  onSubmit() {

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

}
