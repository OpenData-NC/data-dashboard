import MySQLdb
import requests
import json

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
    
def make_address_json(addresses):
    records = {'records':[]}
    count = 1
    for address in addresses:
        address = make_intersection(address)
        item = {'attributes': {'OBJECTID': count,'SingleLine':address}}
        records['records'].append(item)
        count += 1
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

#those with just addresses need to be done singly
county = 'New Hanover'
text = '1701 Oxford Rd'
ll = county_centroids[county]
print geocode(find_url,text,ll,token)

#these are batched
to_geocode = ['400 Wood Green Dr., Wendell, NC','1406 Pisgah Hwy, Candler, NC','28 Florian Way, Fletcher, NC']
address_json = make_address_json(to_geocode)
print batch_geocode(batch_url,address_json,token)

