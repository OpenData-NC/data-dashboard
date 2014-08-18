__author__ = 'vaughn'
#!/usr/bin/env python

import MySQLdb
import requests
import json
import re

user = 'crimeloader'
pw = 'redaolemirc'
db = 'crime'

data_tables = ['accidents','arrests','citations','incidents']


id = 'Jh9RZLWe2B6Yz2eU'
secret = '616f668608064d25a26f1741c73788cb'
auth_url = 'https://www.arcgis.com/sharing/oauth2/token'
single_url = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find'
batch_url = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/geocodeAddresses'

#minutes in a day
#expire = 60 * 24

connection = MySQLdb.connect(user=user,passwd=pw,db=db)
cursor = connection.cursor()

def make_county_centroids():
    county_centroids = {}
    cursor.execute('select county_name, concat_ws(",",min_lon,min_lat,max_lon,max_lat) from county_centers')
    rows = cursor.fetchall()
    for row in rows:
        county_centroids[row[0]] = row[1]
    return county_centroids


def get_token(url,id,secret,expire=None):
    payload = {'client_id': id, 'client_secret': secret,'grant_type':'client_credentials','f':'pjson'}
    if expire:
        payload['expiration'] = str(expire)
    response = requests.get(url,params=payload)
    return json.loads(response.text)['access_token']

#for those with no city info
def single_geocode(text,ll,token):
    address = make_intersection(text)
    payload = {'category':'Address','text':address,'f':'pjson','outfields':'*'}
    if token:
        payload['forStorage'] = 'true'
        payload['token'] = token
    if ll:
        payload['bbox'] = ll
    response = requests.get(single_url, params=payload)
    return json.loads(response.text)

#for those with city,state
def batch_geocode(url,items,token):
    payload = {'category': 'Point Address,Street Address,Intersection','addresses':items,'f':'pjson','sourceCountry':'USA','token':token}
    response = requests.get(url, params=payload)
    return json.loads(response.text)

def batch_make_address_json(rows):
    records = {'records':[]}
    count = 1
    for row in rows:
        address = make_intersection(row[3])
        item = {'attributes': {'OBJECTID': count,'SingleLine':address}}
        records['records'].append(item)
        count = count + 1
    return json.dumps(records)

def make_intersection(text):
    if text.find("/") != -1:
        text = text.replace("/"," & ")
    return text

#check if we've already geocoded this one
#if so, we'll use that data without hitting the api
def check_already_geocoded(text,county):
    cursor.execute("""SELECT * from geocoded_addresses where county=%s and original_address=%s""",(county,text,))
    result = cursor.fetchone()
    return result

#to use with no city or state info
#we'll restrict address search to near county center
#oath toaken

#this is just for testing

def fetch_to_be_geocoded_batch(table, limit=10):
    sql = 'SELECT record_id, agency, county, address from ' + table + " where lat=0 and lon=0 and address like '%, NC' and address not like '% county, nc' limit " + str(limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def fetch_to_be_geocoded_single(table, limit=10):
    sql = 'SELECT record_id, agency, county, address from ' + table + " where lat=0 and lon=0 and address not like '%, NC' and address not like '%restricted%' and address is not null and address != '' limit " + str(limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def find_address(full_address, city):
    address_pattern = '(?P<address>^.+), ' + city
    m = re.compile(address_pattern)
    matches = m.search(full_address)
    return matches.groupdict()['address']


def load_batch_geocoded(geocoded,rows,data_table,geocoder):
    for location in geocoded['locations']:
        geocoder_score = location['score']
        if geocoder_score < 90:
#            print location['score']
#            print data_table, rows[location['attributes']['ResultID'] - 1]
            continue
        index = location['attributes']['ResultID'] - 1
        record_id = rows[index][0]
        agency = rows[index][1]
        county = rows[index][2]
        original_address = rows[index][3]
        city = location['attributes']['City']
        address = location['address']
        street_address = find_address(address, city)
        zip = int(location['attributes']['Postal'])
        lat = float(location['location']['y'])
        lon = float(location['location']['x'])
        sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f, address = "%s" where record_id = "%s" and agency = "%s" limit 1' % (data_table,street_address,city,int(zip),float(lat),float(lon),address,record_id,agency)
        print sql
        # cursor.execute(sql)
        # connection.commit()
        add_address(county, agency, original_address, street_address, address, city, int(zip), float(lat), float(lon), geocoder, geocoder_score)

def load_single_geocoded(location, row, data_table, geocoder):
    geocoder_score = location['feature']['attributes']['Score']
    if geocoder_score < 90:
#        print location['feature']['attributes']['Score']
#        print data_table, row
        return
    record_id = row[0]
    agency = row[1]
    county = row[2]
    original_address = row[3]
    city = location['feature']['attributes']['City1']
    address = location['name']
    street_address = find_address(address, city)
    zip = int(location['feature']['attributes']['Postal1'])
    lat = float(location['feature']['geometry']['y'])
    lon = float(location['feature']['geometry']['x'])
    sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f, address = "%s" where record_id = "%s" and agency = "%s" limit 1' % (data_table,street_address,city,int(zip),float(lat),float(lon),address,record_id,agency)
    print sql
    # cursor.execute(sql)
    # connection.commit()
    add_address(county, agency, original_address, street_address, address, city, int(zip), float(lat), float(lon), geocoder, geocoder_score)


def add_address(county, agency,address, street_address, full_address, city, zip, lat, lon, geocoder, geocoder_score):
    sql = 'insert into already_geocoded (county,agency,original_address,standardized_address,full_address,city,state,zip,lat,lon,geocoder, score) values\
        ("%s","%s","%s","%s","%s", ""%s",%i,%f,%f,"%s",%f)' % (county, agency,address, street_address, full_address, city, zip, lat, lon, geocoder, geocoder_score)
    print sql


def already_geocoded(row):
    agency = row[1]
    county = row[2]
    record_id = row[3]
    sql = 'select standardized_address, city, zip, lat, lon, standardized_full_address from already_geocoded where agency = "%s" and county = "%s" and original_address = %s' \
        % (agency, county, record_id)
    cursor.execute(sql)
    result = cursor.all()
    if len(result):
        update_record(result,row)
        return True
    return False

def update_record(data_table, update, row):
    values = (data_table) + (update) + (row[1],row[2])
    sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f, address = "%s" where record_id = "%s" and agency = "%s" limit 1' \
          % values
    print sql

def main():
    token = get_token(auth_url,id,secret)
    county_centroids = make_county_centroids()
    geocoder = 'ArcGIS Online'
    for data_table in data_tables:
        #for those with full address, including city and state
        batch_rows = fetch_to_be_geocoded_batch(data_table)
        if (batch_rows):
            batch_address_json = batch_make_address_json(batch_rows)
            batch_geocoded = batch_geocode(batch_url,batch_address_json,token)
            load_batch_geocoded(batch_geocoded, batch_rows, data_table,geocoder)

        #for those with just street address
        else:
            single_rows = fetch_to_be_geocoded_single(data_table)
            for row in single_rows:
                if not already_geocoded(row):
                    ll = county_centroids[row[2]]
                    single_geocoded = single_geocode(row[3], ll, token)
                    if len(single_geocoded['locations']):
                        load_single_geocoded(single_geocoded['locations'][0], row,data_table,geocoder)



if __name__ == "__main__":
    main()

