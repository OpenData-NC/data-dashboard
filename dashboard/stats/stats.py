#!/usr/bin/env python
import stats_config as config
import MySQLdb
import json
from slugify import slugify
import decimal
import datetime

user = 'dataDa5h'
pw = 'UnC0p3n'
db = 'crime'
host = '10.240.220.181'
connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
cursor = connection.cursor()

def date_range(table, county=None):
    if table not in config.date_fields:
        return None
    if table in config.no_county:
        county = None

    date_field = config.date_fields[table]
    sql = "select date(max(%s)) maxdate, date(date_add(max(%s), interval -30 day)) mindate, date_format(max(%s),'%%m/%%d/%%Y') max_format, date_format(date_add(max(%s), interval -30 day),'%%m/%%d/%%Y') min_format from %s "
    if table in config.joins:
        sql+= config.joins[table]
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
    if table not in config.select_all:
        return False
    if this_type not in config.select_all[table]:
        return False
    select_fields = config.select_all[table][this_type]
#    params = [select_fields, table]
    join = ''
    group_order_limit = ''
    if table in config.joins:
        join = config.joins[table]
    params.append(join)    
    if table in config.no_county:
        county = None
    if table in config.date_fields:
        date_field = config.date_fields[table]
#        params = params + [date_field, max_min[0], date_field, max_min[1]]
#    if county:
#        params.append(county)
    if table in config.groups_orders_limits:
        if this_type in config.groups_orders_limits[table]:
            group_order_limit = config.groups_orders_limits[table][this_type]
#    params.append(group_order_limit)
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
#            print sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], county, group_order_limit)
            cursor.execute(sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], county, group_order_limit))
        else:
#            print sql % (select_fields, table, join, county, group_order_limit)
            cursor.execute(sql % (select_fields, table, join, county, group_order_limit))
        
    else:
#        print sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], group_order_limit)
        cursor.execute(sql % (select_fields, table, join, date_field, max_min[0], date_field, max_min[1], group_order_limit))    
    rows = cursor.fetchall()
    cols = [ d[0] for d in cursor.description ]
    rows = [ convert_data(row) for row in rows ]
    data = {'headings': cols, 'rows': rows}
    return data


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
    for county in config.counties:
        output_file = output_dir + slugify(county) + '/summary.json'
        response = {}
        for table in config.counties[county]:
            return_type = config.return_types[table]
            response[return_type] = {}
            max_min = date_range(table, county)
            for this_type in config.data_types[table]:
                response[return_type][this_type] = {}
                if max_min:
                    response[return_type][this_type]['date ranges'] = dict(zip(['end','start'], max_min[-2:]))
                response[return_type][this_type]['data'] = query_data(table, max_min, this_type, county)
        with open(output_file, 'w') as output:
            output.write(json.dumps(response, indent=4, sort_keys=True))
    connection.close()
    