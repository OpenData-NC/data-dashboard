import MySQLdb
import requests
import json
import re

user = 'crimeloader'
pw = 'redaolemirc'
db = 'crime'
table = 'county_centers'

id = 'Jh9RZLWe2B6Yz2eU'
secret = '616f668608064d25a26f1741c73788cb'
auth_url = 'https://www.arcgis.com/sharing/oauth2/token'
find_url = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find'
batch_url = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/geocodeAddresses'
#minutes in a day
#expire = 60 * 24

connection = MySQLdb.connect(user=user,passwd=pw,db=db)
cursor = connection.cursor()

def make_county_centroids():
    county_centers = {}
    cursor.execute("""SELECT * from county_centers""")
    rows = cursor.fetchall()
    for row in rows:
        county_centers[row[1]] = {'lat':str(row[3]),'lon':str(row[2])}
    return county_centers

def get_token(url,id,secret,expire=None):
    payload = {'client_id': id, 'client_secret': secret,'grant_type':'client_credentials','f':'pjson'}
    if expire:
        payload['expiration'] = str(expire)
    response = requests.get(url,params=payload)
    return json.loads(response.text)['access_token']

#for those with no city info
def geocode(url,text,ll,token=None):
    text = make_intersection(text)
    payload = {'text':text,'f':'pjson','outfields':'*'}
    if token:
        payload['forStorage'] = 'true'
        payload['token'] = token
    if ll:
        payload['location'] = ','.join([ll['lon'],ll['lat']])
    response = requests.get(url, params=payload)
    return json.loads(response.text)

#for those with city,state
def batch_geocode(url,items,token):
    payload = {'addresses':items,'f':'pjson','sourceCountry':'USA','token':token}
    response = requests.get(url, params=payload)
    return json.loads(response.text)
    
def make_address_json(rows):
    records = {'records':[]}
    count = 1
    for row in rows:
        address = make_intersection(row[2])
        item = {'attributes': {'OBJECTID': count,'SingleLine':address}}
        records['records'].append(item)
        count = count + 1
    return json.dumps(records)

def make_intersection(text):
    if text.find("/") != -1:
        text = " and ".join(text.split("/"))
    return text

#check if we've already geocoded this one
#if so, we'll use that data without hitting the api	
def check_already_geocoded(text,county):
    cursor.execute("""SELECT * from geocoded_addresses where county=%s and original_address=%s""",(county,text,))
    result = cursor.fetchone()
    return result
	
#to use with no city or state info
#we'll restrict address search to near county center
county_centroids = make_county_centroids()
#oath toaken
token = get_token(auth_url,id,secret)

#this is just for testing

def fetch_to_be_geocoded(table, limit=100):
    sql = 'SELECT record_id, agency, address from ' + table + " where lat=0 and lon=0 and address like '%, NC' limit " + str(limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def find_address(location):
    address_pattern = '(?P<address>^.+), ' + location['attributes']['City']
    m = re.compile(address_pattern)
    matches = m.search(location['address'])
    return matches.groupdict()['address']

#those with just addresses need to be done singly
county = 'New Hanover'
text = '1701 Oxford Rd'
ll = county_centroids[county]
print geocode(find_url,text,ll,token)

exit()

data_table = 'incidents'
rows = fetch_to_be_geocoded('incidents', '10')
address_json = make_address_json(rows)
geocoded = batch_geocode(batch_url,address_json,token)
for location in geocoded['locations']:
    record_id = rows[location['attributes']['ResultID'] - 1][0]
    agency = rows[location['attributes']['ResultID'] - 1][1]
    street_address = find_address(location)
    city = location['attributes']['City']
    zip = int(location['attributes']['Postal'])
    lat = float(location['location']['y'])
    lon = float(location['location']['x'])
    address = location['address']

    print rows[location['attributes']['ResultID'] - 1][2]
    sql = 'update %s set street_address = "%s", city = "%s", zip = %i, lat = %f, lon = %f, address = "%s" where record_id = "%s" and agency = "%s" limit 1' % (data_table,street_address,city,int(zip),float(lat),float(lon),address,record_id,agency)
    print sql
    cursor.execute(sql)
    connection.commit()    
    exit()




