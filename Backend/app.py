from flask import Flask, render_template, url_for, request, redirect
from flask_cors import CORS
from flask import jsonify
from datetime import datetime
import pandas as pd 
import flask
import json
import pymongo
from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import csv

app = Flask(__name__)

# base url
CORS(app, resources={r"/*": {"origins": "*"}})

# connecting to postgreSQL 
connection = psycopg2.connect("host='localhost' port= '5432' dbname='orders' user= 'postgres' password= 'password'")

# connecting to mongoDB
client = pymongo.MongoClient("mongodb+srv://mongodb:mongodb@cluster0.i8jlz.mongodb.net/mydb?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.mydb

# method to render orders
def getOrders(orders):
    
    #get all customers from dynamodb
    customers = db.customers.find()
    customer_companies = db.customer_companies.find()
    output = []
    
    #store all customers 
    for customer in customers:
        output.append({'user_id':customer['user_id'], 'name':customer['name'], 'company_id':customer['company_id']})
    
    for order in orders:
        if order['total_amt']:
            order['total_amt'] = round(order['total_amt'],2)
        if order['del_amt']:
            order['del_amt'] = round(order['del_amt'],2)
        for out in output:
            # replace customer_id with customer name for display
            if(order['customer_id']==out['user_id']):
                order['customer_id'] = out['name']

    return orders

@app.route('/orders', methods=['GET'])
def orders():
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #get all orders
    sql = ("""select order_name, cast(created_at as varchar(30)), 
            total_amt,del_amt, customer_id
            from all_orders""") 
    try:
        cur.execute(sql)
        orders = cur.fetchall()
        orders = getOrders(orders)
    except:
        connection.rollback()
    return jsonify(orders)

@app.route('/filterOrders', methods=['POST','GET'])
def filterOrders():

    orders=[]
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        filt = request.get_json()
        filter = '%'+filt['filt']+'%'
        
        # get orders having given order name or part of order name
        try:
            cur.execute("""select order_name, cast(created_at as varchar(30)), 
            total_amt,del_amt, customer_id  from all_orders 
            where customer_id like (%s) or 
            order_name like (%s);""",(filter,filter))
            orders = cur.fetchall()
        
            orders=getOrders(orders)
        except:
            connection.rollback()

    return jsonify(orders)

@app.route('/filterByDate', methods=['POST','GET'])
def filterByDate():
    orders=[]
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        date = request.get_json()
        startdate = ''
        enddate = ''
        
        try:
        # query for filtering orders by date range
            if(date['startdate'] and date['enddate']):
                cur.execute("""select order_name, cast(created_at as varchar(30)), 
                    total_amt,del_amt, customer_id from all_orders where 
                    created_at between cast(%s as timestamptz)
                    and cast(%s as timestamptz)""",(date['startdate'],date['enddate']))
            #if both start date and end date not given return all orders
            else:
                cur.execute("""select order_name, cast(created_at as varchar(30)), 
                total_amt,del_amt, customer_id
                from all_orders""")
            orders = cur.fetchall()
            orders=getOrders(orders)
        except:
            connection.rollback()
    return jsonify(orders)

if __name__ == "__main__":
    
    app.run(debug=True) 