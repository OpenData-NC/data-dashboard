#!/usr/bin/env python

import requests
import json
import re
import time
import MySQLdb

acceptable_types = ['RANGE_INTERPOLATED', 'ROOFTOP', 'GEOMETRIC_CENTER']
acceptable_location_types =['bus_station', 'transit_station', 'establishment','intersection','street_number','parking','establishment']
url = 'https://maps.googleapis.com/maps/api/geocode/json'
geocoder = 'Google'

user = 'crimeloader'
pw = 'redaolemirc'
db = 'crime'
data_tables = ['arrests','incidents']
connection = MySQLdb.connect(user=user,passwd=pw,db=db)
cursor = connection.cursor()

count = 0
daily_max = 2450

def geocode(row, bbox, data_table):
    global count
    global daily_max
    county = row[2]
    address = row[3]

    if address.find('NC') == -1:
        address = address + ' ' + county + ', NC'
    address = title_case(address, county)
    payload = {'address':address, 'bounds': bbox}

    page = requests.get(url,params=payload)
    try:
       results = json.loads(page.text)
    except ValueError:
        time.sleep(120)
        requests.get(url, params=payload)
        results = json.loads(page.text)

    if results['status'] == 'OVER_QUERY_LIMIT':
        time.sleep(120)
        page = requests.get(url,params=payload)
        results = json.loads(page.text)
    if results['status'] != 'OK':
        return False
    data = results['results'][0]
    geometry = data['geometry']
    address_components = data['address_components']
    formatted_address = data['formatted_address']
    found_types = list(set(acceptable_location_types) & set(data['types']))
    if geometry['location_type'] in acceptable_types or len(found_types):
        address_tuple = make_address_tuple(address_components)
        if not address_tuple:
            failed_geocode(row, geocoder, data_table)
            return
        geometry_tuple = make_geometry_tuple(geometry)
        update = (address_tuple[0], address_tuple[1], address_tuple[4],geometry_tuple[0], geometry_tuple[1])
        update_record(data_table, update, row)
#county, agency, address, street_address, full_address, city, zip, lat, lon, geocoder, geocoder_score
        geocode_add = (row[2],row[1], MySQLdb.escape_string(row[3]),address_tuple[0], formatted_address, address_tuple[1],address_tuple[4]) + geometry_tuple
        add_address(geocode_add)
#        sql_tuple = row +  + (formatted_address,) +
    else:
        failed_geocode(row, geocoder, data_table)
    count += 1
    if count == daily_max:
        exit()
    time.sleep(0.25)


def title_case(s, county):
    if s.find('/') != -1:
        if re.match(r'[0-9]+ ',s):
            pieces = re.split('/', s)
            s = pieces[0] + ', ' + county + ' County, NC'
    s = s.replace('/', ' / ')
    word_list = re.split(' ', s)       #re.split behaves as expected
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word.capitalize())
        fixed = " ".join(final)
    return fixed.replace('/', '&')


def make_county_centroids():
    county_centroids = {}
    cursor.execute('select county_name, concat_ws("|", concat_ws(",",min_lat,min_lon)\
       ,concat(max_lat,max_lon)) from county_centers')
    rows = cursor.fetchall()
    for row in rows:
        county_centroids[row[0]] = row[1]
    return county_centroids


def make_address_tuple(address_components):
    street_number = street_name = city = county = state = zip = ''
    for component in address_components:
        if 'street_number' in component['types']:
            street_number = component['short_name']
        if 'route' in component['types']:
            street_name = component['short_name']
        if 'locality' in component['types']:
            city = component['short_name']
        if 'administrative_area_level_2' in component['types']:
            county = component['short_name']
        if 'administrative_area_level_1' in component['types']:
            state = component['short_name']
        if 'postal_code' in component['types']:
            try:
                zip = int(component['short_name'])
            except:
                return False
    if zip == '':
        return False
    if street_number != '':
        street = ' '.join([street_number, street_name])
    else:
        street = street_name
    return (street, city, county, state, zip)


def make_geometry_tuple(geometry):
    location_type = geometry['location_type']
    lat = geometry['location']['lat']
    lon = geometry['location']['lng']
    return (lat,lon, geocoder,location_type)


def fetch_to_be_geocoded(table, limit=10):
    sql = "SELECT record_id, agency, county, address from %s where \
        lat=0 and lon=0 and address != '' limit %i" % (table, limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def add_address(data):
    sql = 'insert into geocoded_addresses (county,agency,original_address,standardized_address,standardized_full_address,city,zip,lat,lon,geocoder, geocoder_score) values\
        ("%s","%s","%s","%s","%s","%s",%i,%f,%f,"%s","%s")' \
          % (data)
    cursor.execute(sql)
    connection.commit()


def already_geocoded(data_table, row):
    agency = row[1]
    county = row[2]
    original_address = MySQLdb.escape_string(row[3])
    sql = 'select standardized_address, city, zip, lat, lon from geocoded_addresses where agency = "%s" and county = "%s" and original_address = "%s"' \
        % (agency, county, original_address)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        update_record(data_table, result, row)
        return True
    return False

def failed_geocode(row, geocoder, data_table):
    sql = 'update %s set lat = -1, lon= -1  where record_id = "%s" and agency = "%s" and county = "%s" limit 1' \
        % (data_table, row[0], row[1], row[2])
    cursor.execute(sql)
    connection.commit()


def update_record(data_table, update, row):
    values = (data_table,) + update + (row[0], row[1])
    sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f where record_id = "%s" and agency = "%s" limit 1' \
          % values
    cursor.execute(sql)
    connection.commit()

def main():
    county_centroids = make_county_centroids()
    geocoder = 'Google'
    for data_table in data_tables:
        #for those with full address, including city and state
        rows = fetch_to_be_geocoded(data_table, 1250)
        for row in rows:
            if not already_geocoded(data_table, row):
                bbox = county_centroids[row[2]]
                geocode(row, bbox, data_table)



if __name__ == "__main__":
    main()

