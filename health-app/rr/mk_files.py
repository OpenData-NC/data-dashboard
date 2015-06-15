#!/usr/bin/env python
from titlecase import titlecase
import os
import slugify 
import MySQLdb
import json


user = 'vhagerty'
pw = 'snook1eB0y'
db = 'crime'
connection = MySQLdb.connect(user=user, passwd=pw, db=db)
cursor = connection.cursor()
main = 'lib/data'
def store_file(data, path_to_file):
    with open(path_to_file, 'w') as out_file:
        out_file.write(data)


def create_file_name(name, path, county=None):
    if county is not None:
        directory = '/'.join([path,slugify.slugify(county)])
    else:
        directory = path
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = slugify.slugify(name) + '.js'
    return '/'.join([directory,file_name])

def create_file(data,file_name,county=None):
    json_data = json.dumps({'results': data})
    file_name = create_file_name(file_name,main,county)
    store_file(json_data,file_name)

def make_counties():
    
    sql = 'select c_id as county_id,county from rr_counties order by county'
    cursor.execute(sql)
    counties = cursor.fetchall()
    cols = [ d[0] for d in cursor.description ]
    counties = [dict(zip(cols,[county[0],titlecase(county[1])])) for county in counties]
    create_file(counties,'index')
    for county in counties:
        make_county(county['county'])


def make_county(county=None):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id from rr inner join rr_types on (rr.fac_type = rr_types.id)  inner join rr_counties on (c_id=county_id) where county = "%s" and rr.status_code in (select * from rr_status) and type = "Restaurant" group by facility_id order by activity_date desc' % (county)
    cursor.execute(sql)
    facilities = cursor.fetchall()
    facilities = [up(item) for item in facilities]
    create_file(facilities,'index',county)
    for facility in facilities:
        make_facility(facility[-1],county)

    sql = 'select distinct addr_city from rr inner join rr_types on (rr.fac_type = rr_types.id)  inner join rr_counties on (c_id=county_id) where county = "%s" and rr.status_code in (select * from rr_status) and type = "Restaurant" group by facility_id order by activity_date desc' % (county)
    cursor.execute(sql)
    cities = cursor.fetchall()
    for city in cities:
        make_city(city[0], county)

def make_city(city, county):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id from rr inner join rr_types on (rr.fac_type = rr_types.id)  inner join rr_counties on (c_id=county_id) where addr_city = "%s" and rr.status_code in (select * from rr_status) and type = "Restaurant" group by facility_id order by activity_date desc' % (city)
    cursor.execute(sql)
    facilities_upper = cursor.fetchall()
    facilities = []
    for row in facilities_upper:
        facilities.append(up(row))
#    facilities = [uppercase(item) for item in facilities]
    create_file(facilities,city, county)

def make_facility(facility, county):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id, item_comments, county from rr inner join rr_counties on (c_id=county_id) where facility_id = "%s" group by facility_id order by activity_date desc' % (facility)
    cursor.execute(sql)
    facility_data = cursor.fetchone()
    cols = [ d[0] for d in cursor.description ]
    uppers = ['fac_name', 'addr_line1', 'addr_city','county']
    strs = ['fac_name', 'addr_line1', 'addr_city','county','item_comments']
    facility_data = dict(zip(cols, list(facility_data)))
    for string in strs:
        try:
#            facility_data[string] = facility_data[string].encode('utf-8');
            facility_data[string] = facility_data[string].encode('utf-8');
        except:
            fixed_str = ''
            for l in facility_data[string]:
                try:
                    l.encode('utf-8')
                    fixed_str += l
                except:
#                    print "BAD"
#                    print l
#                    print facility_data[string]
                    fixed_str += '&deg;'
            facility_data[string] = fixed_str

    for upper in uppers:
        facility_data[upper] = titlecase(facility_data[upper])
    create_file(facility_data,facility, county)

def up(row):
    uppered = []
    for item in row:
        if(isinstance(item, str)):
            uppered.append(titlecase(item))
        else:
            uppered.append(item)
    return uppered
   
if __name__ == '__main__':
    make_counties()
