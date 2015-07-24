#!/usr/bin/env python

#this script provides access to the search api and allows users to register and manage email alerts
#we have ours set up as a mod_wsgi app. you'll need to customize based on your needs
from flask import Flask, render_template, jsonify, make_response
from titlecase import titlecase
import MySQLdb
import datetime
import sys
import decimal
import datetime
import re

from search_config import *

app = Flask(__name__)

home_dir, db, host, user, pw, insert_user, insert_pw = make_config()

#make sure mod_wsgi can find search_config
sys.path.append(home_dir)


#split the query into a dictionary with the field as key and search string as value
def make_params(query):
    pieces = query.split('|')
    params = {}
    for i in range(0, len(pieces)):
        if(i%2 == 0):
            key = pieces[i]
        else:
            params[key] = pieces[i]
    return params
    

#here's where we build the query based on the params passed by the user    
def build_query(data_type, params):

#search strings matched to how they are queried for each table

#we'll use these to build our query
    query_string = []
    query_vals = []
#find the search items we want from the dict from search_config
    search_items = all_search_items[data_type]
    for param in params:
        if param == 'detail':
            continue;
        if data_type in skip_sellers and (param == 'seller-first-name' or param == 'seller-last-name'):
            continue;
        if param in in_categories:
            query_string.append(search_items[param])
            query_vals.append(format_categories(params[param]))
        if param == 'from-date' and 'to-date' not in params and data_type not in skip_dates:
            query_string.append(search_items['from-date'])
            query_vals.append(params[param])
        if param == 'from-date' and 'to-date' in params and data_type not in skip_dates:
            query_string.append(search_items['to-date'])
            query_vals.append(params['from-date'])
            query_vals.append(params['to-date'])
        if param not in skip_params and param not in in_categories:
            if param == 'county' and data_type in skip_counties:
                continue;
            query_string.append(search_items[param])
            query_vals.append(params[param])
            if data_type in name_counts and param in name_counts[data_type]:
                for i in range(0, name_counts[data_type][param]):
                    query_vals.append(params[param])
    #detail means that the user is looing for detail on a particular record
    if 'detail' in params:
        selects = detail_selects
    else:
        selects = selects
    sql = 'select ' + selects[data_type] + ' from ' + data_type + joins[data_type] + ' where ' + ' and '.join(query_string)
    if 'detail' in params and data_type in order_limit:
        sql += order_limit[data_type]
    else:
        sql += ' limit 20000'
#for debugging
#    return [sql]
#    return query_db(sql)
#note that we return the query we build as part of the json response. this is for debugging purposes
    return query_db(sql, data_type, tuple(query_vals))

#categories are crime categories. they are passed to the api separated by "~".
#here we just format them in a way that we use them in a query like this:
# where category in ("category1","category2" ...)
def format_categories(cats):
    return '"' + cats.replace('~','","') + '"'

#python chokes on some of the data that has unusual characters (possibly copied and pasted from Word).
#we try to encode it, but failing that for now we don't return it.
#lame, I know, but we had other fish to fry.

def clean_data(item):
    try:
        cleaned_item = str(item).encode('utf-8')
    except:
        cleaned_item = ''
    return cleaned_item


#python's mysql api returns certain data as python objects -- dates, etc.
#we need to convert those into formats that can be json-ified
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
    cursor = connection.cursor()
    sql_return = sql % query_vals
    try:
        cursor.execute(sql % query_vals)
    except:
    #for now. should return error and log the problem
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


#just what it says. this is used mainly for email alerts
def login_user(params):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'select * from dash_users where email = "%s" and password = "%s"' % (params['user'], params['password'])
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return False
    return True


#just what it says. this is used mainly for email alerts
def register_user(params):
    connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'insert into dash_users (name, email, password, phone) values ("%s","%s","%s","%s")' % (params['name'], params['user'],params['password'], params['phone'])
    cursor.execute(sql)
    connection.commit()
    if cursor.rowcount == 0:
        return False
    return True


#we try to keep the user from submitting duplicate email alerts.
def check_alert_exists(email, query):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'select * from dash_alerts where email = "%s" and search = "%s"' % (email, query)
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return False
    return True


#just what it says. we store the search params, which are used by dash-alerts.py to look for new data via the search api
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


#show all alerts for a user (based on the email address)
def show_alerts(email):
    connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
    cursor = connection.cursor()
    return_alerts = []
    sql = 'select date_format(added, "%%m/%%d/%%Y") `added`, date_format(last_searched, "%%m/%%d/%%Y") `last_searched`, active, search from dash_alerts where email = "%s" order by added' % (email)
    cursor.execute(sql)
    alerts = list(cursor.fetchall())
    cols = [ d[0] for d in cursor.description ]
    all_alerts = [dict(zip(cols,alert)) for alert in alerts]
    for alert in all_alerts:
        alert['search_params'] = make_query_params(alert['search'])
        return_alerts.append(alert)
    return return_alerts


#convenience functions to allow users to do these two things
def delete_alert(email, search):
    connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'delete from dash_alerts where email = "%s" and search = "%s" limit 1' % (email, search)
    cursor.execute(sql)
    connection.commit()


def pause_alert(email, search, pause):
    connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
    cursor = connection.cursor()
    sql = 'update dash_alerts set active = %i where email = "%s" and search = "%s" limit 1' % (pause, email, search)
    cursor.execute(sql)
    connection.commit()


#query params are submitted as a pipe-delimited string after /search/ in the URL.
#this function transforms that into a dictionary where the key is the data type (table) or field
#this is then used, along with the dictionaries in search_config to construct queries and customize
#functionality is various functions based on the data being queried
def make_query_params(query):
    query_params = query.replace('/search/','').split('|')
    formatted_query_params = []
    how_many = len(query_params)
    for i in range(0, how_many):
        formatted_param = query_params[i]
        if i%2 == 0:
            formatted_param = formatted_param.replace('_', ' ')
            formatted_param = formatted_param.replace('-', ' ')
            formatted_param = formatted_param.capitalize() + ' = '
        else:
            if i != how_many -1:
                formatted_param+= '; '
            
        formatted_query_params.append(formatted_param)
    return ''.join(formatted_query_params)
    

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
#to see user's alerts    
@app.route('/users/<query>',methods = ['GET'])
def make_user(query=None):
    params = make_params(query)
    #we're logging in
    if params['type'] == 'login':
        if login_user(params):
            data = {'success':'yes'}
        else:
            data = {'success': 'no'}
    #showing a user's alerts
    elif params['type'] == 'show-alerts':
        alerts = show_alerts(params['email'])
        data = {'alerts': alerts}
    #default is registering a user
    else:
        if register_user(params):
            data = {'success':'yes'}
        else:
            data = {'success': 'no'}
    return jsonify(data)

@app.route('/modify/<query>',methods = ['GET'])
def modify_alert(query=None):
    #modifying a user's alerts
    alerts = query.split('~')
    for alert in alerts:
        params = make_params(alert)
        if int(params['alert-delete']) == 1:
            delete_alert(params['email'], params['alert-search'].replace('*','|').replace('}','/'))
        else:
            pause_alert(params['email'], params['alert-search'].replace('*','|').replace('}','/'), int(params['alert-pause']))
    alert_text = 'alert'
    if len(alerts) > 1:
        alert_text = 'alerts'
    modified = "{} {} modified".format(str(len(alerts)), alert_text)
    return jsonify({'alerts_modified': modified})
    
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

