#!/usr/bin/env python
import MySQLdb
import json
from slugify import slugify
import decimal
import datetime

from stats_config import *

db, host, user, pw = make_config()
connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
cursor = connection.cursor()

#fetch the beginning and end dates of the most recent 30 days
def date_range(table, county=None):
    if table not in date_fields:
        return None
    if table in no_county:
        county = None

    date_field = date_fields[table]
    sql = "select date(max(%s)) maxdate, date(date_add(max(%s), interval -30 day)) mindate, date_format(max(%s),'%%m/%%d/%%Y') max_format, date_format(date_add(max(%s), interval -30 day),'%%m/%%d/%%Y') min_format from %s "
    if table in joins:
        sql+= joins[table]
    if county:
        sql += " where county = '%s'"
#        print sql % (date_field, date_field, date_field, date_field, table, county)
        cursor.execute(sql % (date_field, date_field, date_field, date_field, table, county))
    else:
#        print sql % (date_field, date_field, date_field, date_field, table)
        cursor.execute(sql % (date_field, date_field, date_field, date_field, table))    
    max_min = [str(d) for d in cursor.fetchone()]
    return max_min


def query_data(table, max_min, this_type='all', county=None):
#this horrible mess of a function needs to be cleaned up
    if table not in select_all:
        return False
    if this_type not in select_all[table]:
        return False
    select_fields = select_all[table][this_type]
    join = ''
    group_order_limit = ''
    if table in joins:
        join = joins[table]
    if table in no_county:
        county = None
    if table in date_fields:
        date_field = date_fields[table]
    if table in groups_orders_limits:
        if this_type in groups_orders_limits[table]:
            group_order_limit = groups_orders_limits[table][this_type]
    sql = "select %s from %s %s where "
    if max_min:
        sql+= "%s <= '%s' and date(%s) >= '%s'"
    if county:
        if max_min:
            sql += " and county = '%s'"
        else:
            if table == 'nc_voters_new':
                sql += " county_desc = '%s'"
            else:
                sql += " county = '%s'"
    if group_order_limit != '':
        sql += " %s"
    if county:
        if max_min:
            cursor.execute(sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], county, group_order_limit))
        else:
            cursor.execute(sql % (select_fields, table, join, county, group_order_limit))
        
    else:
        cursor.execute(sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], group_order_limit))    
    rows = cursor.fetchall()
    cols = [ d[0] for d in cursor.description ]
    rows = [ convert_data(row) for row in rows ]
    data = {'headings': cols, 'rows': rows}
    return data

#python's mysql api returns certain data as python objects -- dates, etc.
#we need to convert those into formats that can be json-ified
def convert_data(row):
    converted = []
    for item in row:
        if isinstance(item, decimal.Decimal):
            item = float(item)
        if isinstance(item, datetime.date):
            item = str(item)
        converted.append(item)
    return converted

if __name__ == '__main__':
    output_dir = ''
    response = {}
    for county in counties:
        output_file = output_dir + slugify(county) + '/summary.json'
        response = {}
        for table in counties[county]:
            return_type = return_types[table]
            response[return_type] = {}
            response[return_type]['data-source'] = table
            max_min = date_range(table, county)
            for this_type in data_types[table]:
                response[return_type][this_type] = {}
                if max_min:
                    response[return_type][this_type]['date ranges'] = dict(zip(['end','start'], max_min[-2:]))
                response[return_type][this_type]['data'] = query_data(table, max_min, this_type, county)
        with open(output_file, 'w') as output:
#            output.write(json.dumps(response, indent=4, sort_keys=True))
            output.write(json.dumps(response))
    connection.close()
    