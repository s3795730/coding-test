import pymongo
from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import csv
import pandas as pd 

# connecting to postgreSQL 
connection = psycopg2.connect("host='localhost' port= '5432' dbname='orders' user= 'postgres' password= 'password'")
connection.autocommit = True
cursor = connection.cursor()

# connecting to mongoDB
client = pymongo.MongoClient("mongodb+srv://mongodb:mongodb@cluster0.i8jlz.mongodb.net/mydb?retryWrites=true&w=majority")
# collection mydb from mongoDB
db = client.mydb

# create orders in postgreSQL
def create_orders():
    create_table = "CREATE TABLE orders(id INTEGER PRIMARY KEY NOT NULL,created_at TIMESTAMPTZ, order_name VARCHAR(40), customer_id VARCHAR(50) )"
    cursor.execute(create_table)

# create order_ items in postgreSQL 
def create_order_items():
    create_table = "CREATE TABLE order_items(id INTEGER PRIMARY KEY NOT NULL,order_id INTEGER NOT NULL, price_per_unit FLOAT(8), quantity INTEGER , product VARCHAR(50) )"

    cursor.execute(create_table)

# create deliveries table in postgreSQL 
def create_deliveries():
        create_table = "CREATE TABLE deliveries(id INTEGER PRIMARY KEY NOT NULL,order_item_id INTEGER NOT NULL, delivered_quantity INTEGER NOT NULL)"
        cursor.execute(create_table)

# insert order_items from csv
def insert_order_items():
    #open given csv
    with open('./data/Test task - Postgres - order_items.csv', newline='', encoding="utf8") as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile)
        # insert each row of csv
        for row in spamreader:

            sql = "INSERT INTO order_items(id,order_id, price_per_unit,quantity, product) VALUES ('%s','%s', '%s', '%s','%s' );" % (row[0], row[1], row[2], row[3],row[4])
            try:
                cursor.execute(sql)
                connection.commit()
            except:
                connection.rollback()

# insert orders from csv
def insert_orders():
    with open('./data/Test task - Postgres - orders.csv', newline='', encoding="utf8") as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile)
        for row in spamreader:

            sql = "INSERT INTO orders(id, created_at, order_name, customer_id) VALUES ('%s','%s', '%s', '%s' );" % (row[0], row[1], row[2], row[3])
            try:
                cursor.execute(sql)
            except:
                connection.rollback()

# insert orders from csv
def insert_deliveries():
    with open('./data/Test task - Postgres - deliveries.csv', newline='', encoding="utf8") as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile)
        for row in spamreader:

            sql = "INSERT INTO deliveries(id, order_item_id, delivered_quantity) VALUES ('%s','%s', '%s');" % (row[0], row[1], row[2])
            try:
                cursor.execute(sql)
                # connection.commit()
            except:
                connection.rollback()

# create a view by integrating all tables 
# to retrieve data directly from view
def view_all_orders():
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = ("""DROP VIEW IF EXISTS all_orders;
        create view all_orders as select ord.order_name, orders.created_at,ord.total_amt, ord.del_amt,  orders.customer_id
        from(select o.order_name,sum(amt.total_amt) as total_amt, sum(amt.del_amt) as del_amt
        from (select oi.id, oi.order_id, oi.price_per_unit, oi.quantity, oi.product, 
        oi.price_per_unit*oi.quantity as total_amt, 
        sum (d.delivered_quantity)*oi.price_per_unit as del_amt
        from order_items as oi 
        Left Join deliveries as d on oi.id = d.order_item_id 
        group by oi.id) as amt 
        Inner Join orders as o on amt.order_id = o.id
        group by amt.order_id, o.order_name
        order by amt.order_id) as ord
        Inner Join orders on ord.order_name = orders.order_name;""")

    cur.execute(sql)

# insert data to orders in mongoDB
def add_to_orders():
    data = pd.read_csv('./data/Test task - Orders.csv')
    records = data.to_dict(orient = 'records')
    db.orders.insert_many(records)

# insert data to customer_companies in mongoDB
def add_to_cust_company():
    data = pd.read_csv('./data/Test task - Mongo - customer_companies.csv')
    records = data.to_dict(orient = 'records')
    db.customer_companies.insert_many(records)

# insert data to customers in mongoDB
def add_to_customers():
    data = pd.read_csv('./data/Test task - Mongo - customers.csv')
    records = data.to_dict(orient = 'records')
    db.customers.insert_many(records)

create_orders()
create_order_items()
create_deliveries()
insert_order_items()
insert_orders()
insert_deliveries()
view_all_orders()
add_to_orders()
add_to_customers()
add_to_cust_company()

# close cursor and connection to postgreSQL
cursor.close()
connection.close()