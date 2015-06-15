#!/usr/bin/env python
from flask import Flask, render_template, jsonify
from titlecase import titlecase
import MySQLdb


app = Flask(__name__)

user = 'crimeloader'
pw = 'redaolemirc'
db = 'crime'
connection = MySQLdb.connect(user=user, passwd=pw, db=db)
cursor = connection.cursor()

@app.route('/')
def make_index():
    
    sql = 'select c_id as county_id,county from counties order by county'
    cursor.execute(sql)
    counties = cursor.fetchall()
    cols = [ d[0] for d in cursor.description ]
    counties = [dict(zip(cols,[county[0],titlecase(county[1])])) for county in counties]
    return jsonify(results=counties)


@app.route('/county/<county>')
def county(county=None):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id from rr inner join rr_types on (rr.fac_type = rr_types.id)  inner join counties on (c_id=county_id) where county = "%s" and rr.status_code in (select * from rr_status) and type = "Restaurant" group by facility_id order by activity_date desc' % (county)
    cursor.execute(sql)
    facilities = cursor.fetchall()
    facilities = [up(item) for item in facilities]
    return jsonify(results=facilities)

@app.route('/city/<city>')
def city(city=None):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id from rr inner join rr_types on (rr.fac_type = rr_types.id)  inner join counties on (c_id=county_id) where addr_city = "%s" and rr.status_code in (select * from rr_status) and type = "Restaurant" group by facility_id order by activity_date desc' % (city)
    cursor.execute(sql)
    facilities_upper = cursor.fetchall()
    facilities = []
    for row in facilities_upper:
        facilities.append(up(row))
#    facilities = [uppercase(item) for item in facilities]
    return jsonify(results=facilities)

@app.route('/facility/<facility>')
def facility(facility=None):
    sql = 'select fac_name, addr_line1, addr_city, date_format(activity_date, "%%m/%%d/%%Y") as  activity_date, activity_final_score as score, rr.facility_id as facility_id, item_comments, county from rr inner join counties on (c_id=county_id) where facility_id = "%s" group by facility_id order by activity_date desc' % (facility)
    cursor.execute(sql)
    facility = cursor.fetchone()
    cols = [ d[0] for d in cursor.description ]
    uppers = ['fac_name', 'addr_line1', 'addr_city','county']
    facility = dict(zip(cols, list(facility)))
    for upper in uppers:
        facility[upper] = titlecase(facility[upper])
    return jsonify(results=facility)

def up(row):
    uppered = []
    for item in row:
        if(isinstance(item, str)):
            uppered.append(titlecase(item))
        else:
            uppered.append(item)
    return uppered
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
