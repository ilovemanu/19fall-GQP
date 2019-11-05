# 19fall_GQP_MassDEP

TO-DO: Project description.

## Data Processing and Exploration

File Conversion
- Make sure pdf_to_txt.py and batch_pdf_to_txt.py are in the same directory with the folder containing pdf files.
- Run batch_pdf_to_txt.py for folder to folder processing.

Parsing
- 1_dataprocess_elements.ipynb
- file_parser.py
- parser_alex.py

Cleaning
- deep_clean.py
- ...

Combining
- ...

Exploratory Data Analysis
- ...

## Getting Started with the Web Application

### Prerequisites

- Elasticsearch installation.
https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

- Start Elasticsearch.
Run `elasticsearch` from the command line.

- Elasticsearch-browser installation.
Elasticsearch-browser is needed for the front-end. MacOS:
```
npm install elasticsearch-browser
```

### Installing

1. Download the 19fall-GQP repository.

2. CSV files are included in the `/data` folder. To import data into Elasticsearch, first make sure Elasticsearch is connected, then run 
```
/src/es-load.py
```

3. Install dependencies, go to `/web` and run
```
npm install
```

4. To start the web app, under `/web` run `ng serve`. Navigate to `http://localhost:4200/`.


## Built With
This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 6.0.3.


## Authors


## License


## Acknowledgments

