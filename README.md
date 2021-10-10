# Order Viewing Application

## Introduction:

A simple application to view orders and its specific details.
Orders can be filtered by order name, customer id and date range.  
## Pre-requisites:

1. PostgreSQL with user: postgres, password: password, database: orders
2. python3

## Running the application locally:

1. cd into Backend
2. run `pip install -r requirements.txt`
3. run `python3 initialize.py` for initializing the databases
4. run `python3 app.py`
5. cd into Frontend/frontend
6. run `npm run serve`
7. go to your web browser at "http://localhost:8080/orders"
