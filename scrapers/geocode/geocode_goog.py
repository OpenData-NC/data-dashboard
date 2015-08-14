#!/usr/bin/env python

#script to attempt to try to attach lat/lon coords to data using google's geocode api
#ungeocoded data has zeros for these fields. 
#we use -1 for those where the geocoder failed for some reason so we don't try those again

import requests
import json
import re
import time
import MySQLdb

from scraper_config import make_config

#we only need db, user and pw to connect to the database
home_dir, data_dir, db, user, pw, commands_url = make_config('')

#these are values returned by the geocode api. any result that isn't among these types/location_types
#is considered a failure
acceptable_types = ['RANGE_INTERPOLATED', 'ROOFTOP', 'GEOMETRIC_CENTER']
acceptable_location_types =['bus_station', 'transit_station', 'establishment','intersection','street_number','parking','establishment']

url = 'https://maps.googleapis.com/maps/api/geocode/json'

#a value we add to the record to indicate the source of the lat/lon
geocoder = 'Google'

#we'll geocode data from tables in this list
data_tables = ['arrests','incidents']

#the database connection we'll use
connection = MySQLdb.connect(user=user,passwd=pw,db=db)
cursor = connection.cursor()

#google limits us to 2,500 calls but we try to stay under that
count = 0
daily_max = 2450


#try to geocode an address
#in addition to county and address,
#row contains the agency and the record_id,
#those constitute the primary key in the table
#we'll use those to update the data in data_table
#bbox is the county bounding box, to increase google's accuracy

def geocode(row, bbox, data_table):
    global count
    global daily_max
    county = row[2]
    address = row[3]

#try to format the address to increase the chances of success
    if address.find('NC') == -1:
        address = address + ' ' + county + ', NC'
    address = title_case(address, county)
    
    payload = {'address':address, 'bounds': bbox}
    page = requests.get(url,params=payload)
    
#try to convert the results. if it fails for some reason, assume google says we're over our rate limit, so we pause
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
        
#google choked on this address. assume it's bad
    if results['status'] != 'OK':
        return False
#the actual results are returned in an array, sometimes with multiple results.
#we assume the first one is the best.
#we assign the various components to variables to simplify the code
    data = results['results'][0]
    geometry = data['geometry']
    address_components = data['address_components']
    formatted_address = data['formatted_address']
    
#test the result to see if it's among our acceptable types
    found_types = list(set(acceptable_location_types) & set(data['types']))
    if geometry['location_type'] in acceptable_types or len(found_types):
#test the address to see if it has what we need. if not, return false.
#otherwise return a tuple of the components that we'll use to update the data
        address_tuple = make_address_tuple(address_components)
        if not address_tuple:
            failed_geocode(row, geocoder, data_table)
            return
#pull out the latitude and longitude
        geometry_tuple = make_geometry_tuple(geometry)
#update the record with data from google        
        update = (address_tuple[0], address_tuple[1], address_tuple[4],geometry_tuple[0], geometry_tuple[1])
        update_record(data_table, update, row)
#add this address to the table of those we've seen in past geocode attempts. 
#if we encounter this address again, we'll just use this information rather than hit google
        geocode_add = (row[2],row[1], MySQLdb.escape_string(row[3]),address_tuple[0], formatted_address, address_tuple[1],address_tuple[4]) + geometry_tuple
        add_address(geocode_add)
    else:
#we failed to geocode this address, so flag it
        failed_geocode(row, geocoder, data_table)
#quit if we've reached our daily limit
#otherwise, sleep for a quarter second and move on
    count += 1
    if count == daily_max:
        exit()
    time.sleep(0.25)

#in addition to making the address title case to try to increase google's accuracy,
#we try to account for oddness such as slashes in addresses, which we replace with an ampersand
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


#we use a bounding box of of the county to try to increase google's accuracy. this info
#comes from a table we created. It's a dictionary keyed by county name
def make_county_centroids():
    county_centroids = {}
    cursor.execute('select county_name, concat_ws("|", concat_ws(",",min_lat,min_lon)\
       ,concat(max_lat,max_lon)) from county_centers')
    rows = cursor.fetchall()
    for row in rows:
        county_centroids[row[0]] = row[1]
    return county_centroids


#google returns addresses in a variety of formats, depending on the address
#we test for those and construct a tuple. if there's no zip code, something's wrong
#so we flag it as a failure by returning False

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


#moved to here just to try to simply the main geocoder function
def make_geometry_tuple(geometry):
    location_type = geometry['location_type']
    lat = geometry['location']['lat']
    lon = geometry['location']['lng']
    return (lat,lon, geocoder,location_type)


#grab those we want to geocode
def fetch_to_be_geocoded(table, limit=10):
    sql = "SELECT record_id, agency, county, address from %s where \
        lat=0 and lon=0 and address != '' limit %i" % (table, limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


#add successful geocode data. we check this table before hitting google. if an address matches, we'll use this geocode info instead
def add_address(data):
    sql = 'insert into geocoded_addresses (county,agency,original_address,standardized_address,standardized_full_address,city,zip,lat,lon,geocoder, geocoder_score) values\
        ("%s","%s","%s","%s","%s","%s",%i,%f,%f,"%s","%s")' \
          % (data)
    cursor.execute(sql)
    connection.commit()


#if we'lve already geocoded this address for a different record, use the data we stored that time.
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


#set the lat/lons on a record where geocoding failed to -1. that way, we won't try it again
def failed_geocode(row, geocoder, data_table):
    sql = 'update %s set lat = -1, lon= -1  where record_id = "%s" and agency = "%s" and county = "%s" limit 1' \
        % (data_table, row[0], row[1], row[2])
    cursor.execute(sql)
    connection.commit()

    
#update the record with our geocoded data
def update_record(data_table, update, row):
    values = (data_table,) + update + (row[0], row[1])
    sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f where record_id = "%s" and agency = "%s" limit 1' \
          % values
    cursor.execute(sql)
    connection.commit()

    
def main():
#make a dictionary with our county bounding boxes, which we'll pass to google
    county_centroids = make_county_centroids()
    geocoder = 'Google'
#limit the number of records we'll attempt to geocode. we'll split it equally among all the data tables we'll be trying 
    limit = int(max/len(data_tables))
    for data_table in data_tables:
        #for those with full address, including city and state
        rows = fetch_to_be_geocoded(data_table, limit)
        for row in rows:
            if not already_geocoded(data_table, row):
                bbox = county_centroids[row[2]]
                geocode(row, bbox, data_table)



if __name__ == "__main__":
    main()

