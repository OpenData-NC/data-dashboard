#!/usr/bin/env python
from flask import Flask, render_template, jsonify, make_response
from titlecase import titlecase
import MySQLdb
import datetime
import sys
sys.path.append('/home/vaughn.hagerty/search')
import decimal
import datetime
import re

import search_config as config

app = Flask(__name__)

user = 'dataDa5h'
pw = 'UnC0p3n'
db = 'crime'
insert_user = 'crimeloader'
insert_pw = 'redaolemirc'
host = '10.240.220.181'
#connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
#connection = MySQLdb.connect(user=user, passwd=pw, db=db)
#cursor = connection.cursor()

#split the query into a dictionary with the field as key and search string as value
def make_params(query):
    pieces = query.split('|')
    params = {}
    for i in range(0, len(pieces)):
        if(i%2 == 0):
            key = pieces[i]
        else:
            params[key] = pieces[i]
#    if 'data-types' in params:
    return params
    
    
def build_query(data_type, params):

#search strings matched to how they are queried for each table

#we'll use these to build our query
    query_string = []
    query_vals = []
#find the search items we want from the dict from search_config
    search_items = config.all_search_items[data_type]
    for param in params:
        if param == 'detail':
            continue;
        if data_type in config.skip_sellers and (param == 'seller-first-name' or param == 'seller-last-name'):
            continue;
        if param in config.in_categories:
            query_string.append(search_items[param])
            query_vals.append(format_categories(params[param]))
        if param == 'from-date' and 'to-date' not in params and data_type not in config.skip_dates:
            query_string.append(search_items['from-date'])
            query_vals.append(params[param])
        if param == 'from-date' and 'to-date' in params and data_type not in config.skip_dates:
            query_string.append(search_items['to-date'])
            query_vals.append(params['from-date'])
            query_vals.append(params['to-date'])
        if param not in config.skip_params and param not in config.in_categories:
            if param == 'county' and data_type in config.skip_counties:
                continue;
            query_string.append(search_items[param])
            query_vals.append(params[param])
            if data_type in config.name_counts and param in config.name_counts[data_type]:
                for i in range(0, config.name_counts[data_type][param]):
                    query_vals.append(params[param])
    if 'detail' in params:
        selects = config.detail_selects
    else:
        selects = config.selects
    sql = 'select ' + selects[data_type] + ' from ' + data_type + config.joins[data_type] + ' where ' + ' and '.join(query_string)
    if 'detail' in params and data_type in config.order_limit:
        sql += config.order_limit[data_type]
    else:
        sql += ' limit 20000'
#for debugging
#    return [sql]
#    return query_db(sql)
    return query_db(sql, data_type, tuple(query_vals))


def format_categories(cats):
    return '"' + cats.replace('~','","') + '"'

#python chokes on some of the data that has unusual characters (possibly copied and pasted from Word).
#we try to encode it, but failing that for now we don't return it.
#we'll need to try to address this later.

def clean_data(item):
    try:
        cleaned_item = str(item).encode('utf-8')
    except:
        cleaned_item = ''
    return cleaned_item

def convert_data(row):
    converted = []
    for item in row:
        if isinstance(item, decimal.Decimal):
            item = float(item)
        if isinstance(item, datetime.date):
            item = str(item)
        if isinstance(item, basestring):
            try:
                item = item.encode('utf-8','ignore')
            except:
                item = ''
        converted.append(item)
    return converted
    
#execute our query and return the data    
def query_db(sql, data_type, query_vals):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
#connection = MySQLdb.connect(user=user, passwd=pw, db=db)
    cursor = connection.cursor()
    sql_return = sql % query_vals
#    cursor.execute(sql + ' limit 1000')
    try:
        cursor.execute(sql % query_vals)
    except:
    #for now. should return error
        log(sql_return, 'Failed query')
        connection.close()
        return {'headings':[], 'data': [], 'sql': sql_return}
    formatted_data = []
#we'll need the field names for headings in the json
    cols = [ d[0] for d in cursor.description ]
    data = cursor.fetchall()
    for row in data:
        cleaned_row = convert_data(row)
        formatted_data.append(cleaned_row)
    connection.close()
    return { 'headings': cols, 'data': formatted_data , 'data_source': data_type, 'sql': sql_return}


def login_user(params):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'select * from dash_users where email = "%s" and password = "%s"' % (params['user'], params['password'])
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return False
    return True


def register_user(params):
    connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'insert into dash_users (name, email, password, phone) values ("%s","%s","%s","%s")' % (params['name'], params['user'],params['password'], params['phone'])
    cursor.execute(sql)
    connection.commit()
    if cursor.rowcount == 0:
        return False
    return True

def check_alert_exists(email, query):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'select * from dash_alerts where email = "%s" and search = "%s"' % (email, query)
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return False
    return True

def add_alert(email, query):
    connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
    cursor = connection.cursor()
    alert_exists = check_alert_exists(email, query)
    if(alert_exists):
        return "An alert for this search already exists for {}".format(email)
    sql = 'insert dash_alerts (email, added, last_searched, active, search) values("%s",now(),now(),1,"%s")' % (email, query)
    cursor.execute(sql)
    connection.commit()
    if cursor.rowcount == 0:
        return "We were unable to add this search to your alerts. Sorry!"
    return "ok"
    
#our very simplistic routing

@app.route('/<query>',methods = ['GET'])
def make_index(query=None):
#this will hold the data we're returning
    log(query)
    data = {}
    params = make_params(query)
    params['data_types'] = params['data_types'].split('-')
#map the data type requested to the actual table name
    tables = {'voter': 'nc_voters_new',
                'health': 'rr',
                'rr': 'rr',
                'dash_nh_rr': 'dash_nh_rr',
                'dash_nh_property': 'dash_nh_property',
                'dash_nh_real_estate': 'dash_nh_real_estate',
                'dash_buncombe_property': 'dash_buncombe_property',
                'dash_buncombe_real_estate': 'dash_buncombe_real_estate',
                'dash_wake_property': 'dash_wake_property',
                'dash_wake_real_estate': 'dash_wake_real_estate',
                'nc_voters_new': 'nc_voters_new',
                'property-Buncombe': 'dash_buncombe_property',
                'realestate-Buncombe': 'dash_buncombe_real_estate',
                'property-New Hanover': 'dash_nh_property',
                'realestate-New Hanover': 'dash_nh_real_estate',
                'property-Wake': 'dash_buncombe_property',
                'realestate-Wake': 'dash_wake_real_estate',
                'incidents': 'incidents',
                'arrests': 'arrests',
                'accidents': 'accidents',
                'citations': 'citations',
            }
#build the table names used for the queries
#for each data type requested, query and format the results
     
    for data_type in params['data_types']:
#crime actually has four tables. For now we're searching all of them
#though we'll probably let them be searched separately down the line

        if data_type == 'crime':
            for t in ['incidents','arrests','citations','accidents']:
                data[t] = build_query(t, params)
        else:
#use a combination of the county and the requested data type to figure out
#which table to use for property and real estate
            if data_type == 'property' or data_type == 'realestate':
                table_key = '-'.join([data_type,titlecase(params['county'])])
            else:
                table_key = data_type
            data[data_type] = build_query(tables[table_key], params)
            if 'detail' in params:
                data[data_type]['detail'] = 1
#return the json object
        
    return jsonify(results=data)

#to add an alert    
@app.route('/alerts/<query>',methods = ['GET'])
def make_alert(query=None):
    params = make_params(query)
    email = params['user']
    query = '/search/' + re.sub('\|user\|.*','',query)
    alert_result = add_alert(email, query)
    if alert_result == 'ok':
        data = {'success':'yes'}
    else:
        data = {'success': 'no', 'alert_result': alert_result}
    return jsonify(data)

#to register or log in a user    
@app.route('/users/<query>',methods = ['GET'])
def make_user(query=None):
    params = make_params(query)
    if params['type'] == 'login':
        if login_user(params):
            data = {'success':'yes'}
        else:
            data = {'success': 'no'}
    else:
        if register_user(params):
            data = {'success':'yes'}
        else:
            data = {'success': 'no'}
    return jsonify(data)

    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
#not currently used, but a utility to try to format all-caps data
#because we can't always predict what should or shouldn't be capped
#we compromise by making it titlecase

def up(row):
    uppered = []
    for item in row:
        if(isinstance(item, str)):
            uppered.append(titlecase(item))
        else:
            uppered.append(item)
    return uppered

#for debugging
def log(msg, type="query"):
    with open('/var/www/log/wsgi.log', 'a') as l:
        d = datetime.datetime.now()
        l.write("\t".join([msg,type, str(d)]) + "\n")
        l.close()

if __name__ == '__main__':
    app.run()

