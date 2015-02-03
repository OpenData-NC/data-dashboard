#!/usr/bin/env python
from flask import Flask, render_template, jsonify
from titlecase import titlecase
import MySQLdb


app = Flask(__name__)

user = 'dataDa5h'
pw = 'UnC0p3n'
db = 'crime'
host = '10.240.220.181'
connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
#connection = MySQLdb.connect(user=user, passwd=pw, db=db)
cursor = connection.cursor()

#split the query into a dictionary with the field as key and search string as value
def make_params(query):
    pieces = query.split('|')
    params = {}
    for i in range(0, len(pieces)):
        if(i%2 == 0):
            key = pieces[i]
        else:
            params[key] = pieces[i]
    params['data_types'] = params['data_types'].split('-')
    return params
    
    
def build_query(data_type, params):

#search strings matched to how they are queried for each table

    all_search_items = {
        'incidents': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                      'county': 'county = "%s"', 'from-date': 'reported_date = "%s"',
                      'to-date': '(reported_date >= "%s" and reported_date <= "%s")',
                      'street-number': 'address like "%s %%"',
                      'street-name': 'address like "%%%s%%"'},
        'arrests': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                      'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                      'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                      'street-number': 'address like "%s %%"',
                      'street-name': 'address like "%%%s%%"'},
        'citations': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                      'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                      'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                      'street-number': 'address like "%s %%"',
                      'street-name': 'address like "%%%s%%"'},
        'accidents': {'first-name': '(name1 like "%s%%" or name2 like "%s%%)',
                      'last-name': '(name1 like "%% %s" or name2 like "%% %s")',
                      'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                      'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                      'street-number': 'address like "%s %%"',
                      'street-name': 'address like "%%%s%%"'},
        'nc_voters_new': {'first-name': 'first_name like "%s%%"',
                      'last-name': 'last_name = "%s"',
                      'county': 'county_desc = "%s"',
                      'street-number': 'res_street_address like "%s %%"',
                      'street-name': 'res_street_address like "%%%s%%"'},
        'rr': {'first-name': 'fac_name like "%%%s%%"', 'last-name': 'fac_name like "%s%%"',
                      'county': 'county = "%s"', 'from-date': 'activity_date = "%s"',
                      'to-date': '(activity_date >= "%s" and activity_date <= "%s")',
                      'street-number': 'addr_line1 like "%s %%"',
                      'street-name': 'addr_line1 like "%%%s%%"'},
        'dash_buncombe_property': {'first-name': '(owner1_firstname = "%s" or owner2_firstname = "%s")',
                      'last-name': '(owner1_lastname = "%s" or owner2_lastname = "%s")',
                      'from-date': 'deeddate = "%s"',
                      'to-date': '(deeddate >= "%s" and deeddate <= "%s")',
                      'street-number': 'housenum = "%s"',
                      'street-name': 'streetname = "%s"'},
        'dash_buncombe_real_estate': {'first-name': '(seller1_fname = "%s" or seller2_fname = "%s" or buyer1_fname = "%s" or buyer2_fname = "%s")',
                      'last-name': '(seller1_lname = "%s" or seller2_lname = "%s" or buyer1_lname = "%s" or buyer2_lname = "%s")',
                      'from-date': 'selldate = "%s"',
                      'to-date': '(selldate >= "%s" and selldate <= "%s")',
                      'street-number': 'housenum = "%s"',
                      'street-name': 'streetname = "%s"'},

        'dash_nh_property': {'first-name': '(owner like "%s%%" or `co-owner` like "%s%%)',
                      'last-name': '(owner like "%% %s" or `co-owner` like "%% %s")',
                      'street-number': '`situs-num` = "%s"',
                      'street-name': '`situs-street` = "%s"'},

        'dash_nh_real_estate': {'first-name': '(seller like "%s%%" or seller like "%s%%)',
                      'last-name': '(buyer like "%% %s" or buyer like "%% %s")',
                      'from-date': 'sale_date = "%s"',
                      'to-date': '(sale_date >= "%s" and sale_date <= "%s")',
                      'street-number': 'address like "%s %%"',
                      'street-name': 'address like "%%%s%%"'},

        'dash_wake_property': {'first-name': '(owner_line1 like "%s%%" or owner_line2 like "%s%%)',
                      'last-name': '(owner_line1 like "%% %s" or owner_line1 like "%% %s")',
                      'from-date': 'total_sale_date = "%s"',
                      'to-date': '(total_sale_date >= "%s" and total_sale_date <= "%s")',
                      'street-number': 'site_address_street_number = "%s"',
                      'street-name': 'site_address_street_name = "%s"'},

        'dash_wake_real_estate': {'first-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%)',
                      'last-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%")',
                      'from-date': 'total_sale_date = "%s"',
                      'to-date': '(total_sale_date >= "%s" and total_sale_date <= "%s")',
                      'street-number': 'site_address_street_number = " %s"',
                      'street-name': 'site_address_street_name = " %s"'}
    }
#fields we're selecting for return for each table
    selects = {
        'incidents': 'record_id `Record ID`, agency `Agency`, name `Name`, date_format(date_reported,"%m/%d/%Y") `Date reported` , category `Category`, incidents.charge `Charge`, address `Address`',
        'arrests': 'record_id `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, `Category`, arrests.charge `Charge`, address `Address`',
        'citations': 'record_id `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, charge, address `Address`',
        'accidents': 'record_id `Record ID`, agency `Agency`, name1 `Driver 1`, name2 `Driver 2`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, address `Address`',
        'nc_voters_new': 'voter_reg_num `Voter reg. num.`, first_name `First name`, last_name `Last name`, res_street_address `Address` , res_city_desc `City`, zip_code `Zip code`',
        'rr': 'fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%m/%d/%Y") `Insp. date`, activity_final_score `Score`',
        'dash_buncombe_property': 'parcelid `Parcel ID`, concat_ws(" ", owner1_firstname, owner1_lastname) `Owner 1`, concat_ws(" ", owner2_firstname, owner2_lastname) `Owner 2`, date_format(deeddate,"%m/%d/%Y") `Deed date`, concat_ws(" ", housenum, housesuffix, streetdirection, streetname, streettype) `address`, citycode `City code`, taxableval `Tax value`',
        'dash_buncombe_real_estate': 'parcelid `Parcel ID`, concat_ws(" ", seller1_fname, seller1_lname) `Seller 1`, concat_ws(" ", seller2_fname, seller2_lname) `Seller 2`, concat_ws(" ", buyer1_fname, buyer1_lname) `Buyer 1`, concat_ws(" ", buyer2_fname, buyer2_lname) `Buyer 2`,date_format(selldate,"%m/%d/%Y") `Sale date`, concat_ws(" ", housenum, housesuffix, streetdirection, streetname, streettype) `address`, citycode `City code`, sellingprice `Sale price`',
        'dash_nh_property': 'pid `Parcel ID`, owner `Owner 1`, `co-owner` `Owner 2`, concat_ws(" ", `situs-num`, `situs-street`) `Address`, `situs-city` `City code`, `real-assval` `Tax value`',
        'dash_nh_real_estate': 'pid `Parcel ID`, seller `Seller`, buyer `Buyer`, date_format(sale_date,"%m/%d/%Y") `Sale date`, address `Address`, city `City`, price `Sale price`',
        'dash_wake_property': 'pin_num `Parcel ID`, owner_line1 `Owner 1`, owner_line2 `Owner 2`, date_format(deed_date,"%m/%d/%Y") `Deed date`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `address`, city `City code`, sum(building_assessed_value,land_assessed_value) `Tax value`',
        'dash_wake_real_estate': 'pin_num `Parcel ID`, buyer_line1 `Buyer 1`, buyer_line2 `Buyer 2`, date_format(total_sale_date,"%m/%d/%Y") `Sale date`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `address`, city `City code`, total_sale_price `Sale price`'
#        'nc_voters': 'voter_reg_num `Voter reg. num.`, first_name `First name`, last_name `Last name`, res_street_address `Address` , res_city_desc `City`, zip_code `Zip code`, full_phone_number `Phone num.`',
    }
#any joins we might need, such as county name lookups and crime categories

    joins = {
        'incidents': ' inner join charge_categories on incidents.charge = charge_categories.charge',
        'arrests': ' inner join charge_categories on arrests.charge = charge_categories.charge',
        'citations': '',
        'accidents': '',
        'nc_voters_new': '',
        'rr': ' inner join rr_counties on county_id = c_id ',
        'dash_buncombe_property': '',
        'dash_buncombe_real_estate': '',
        'dash_nh_property': '',
        'dash_nh_real_estate': '',
        'dash_wake_property': '',
        'dash_wake_real_estate': ''
        
    }
#find the search items we want from the dict above
    search_items = all_search_items[data_type]
#dictionaries to make the query building below easier
    skip_params = ['from-date','to-date','data_types']
#these tables don't have a date field
    skip_dates = ['nc_voters_new','dash_nh_property']
#some tables have numerous name fields, so we have to account for that when building our query. 
#The number is how many times in addition to the first that we'll use a name string in building a query (e.g. 1 = 2 times, 3 = 4, etc.)
    name_counts = {'accidents': 1, 'dash_buncombe_property': 1, 'dash_buncombe_real_estate': 3,'dash_nh_property': 1, 'dash_nh_real_estate': 1,'dash_wake_property': 1, 'dash_wake_real_estate': 1 }
#we don't use the county in these tables. they don't have a county field because they're already county-specific.
    skip_counties = ['dash_buncombe_property','dash_buncombe_real_estate','dash_nh_property', 'dash_nh_real_estate','dash_wake_property', 'dash_wake_real_estate']
#we'll use these to build our query
    query_string = []
    query_vals = []

    for param in params:
        if param == 'from-date' and 'to-date' not in params and data_type not in skip_dates:
            query_string.append(search_items['from-date'])
            query_vals.append(params[param])
        if param == 'from-date' and 'to-date' in params and data_type not in skip_dates:
            query_string.append(search_items['to-date'])
            query_vals.append(params['from-date'])
            query_vals.append(params['to-date'])
        if param not in skip_params:
            if param == 'county' and data_type in skip_counties:
                continue;
            query_string.append(search_items[param])
            query_vals.append(params[param])
            if data_type in name_counts and (param == 'first-name' or param == 'last-name'):
                for i in range(0, name_counts[data_type]):
#            if data_type == 'accidents' and (param == 'first-name' or param == 'last-name'):
                    query_vals.append(params[param])


    sql = 'select ' + selects[data_type] + ' from ' + data_type + joins[data_type] + ' where ' + ' and '.join(query_string) % tuple(query_vals)
#for debugging
#    return [sql]
    return query_db(sql)

#python chokes on some of the data that has unusual characters (possibly copied and pasted from Word).
#we try to encode it, but failing that for now we don't return it.
#we'll need to try to address this later.

def clean_data(item):
    try:
        cleaned_item = str(item).encode('utf-8')
    except:
        cleaned_item = ''
    return cleaned_item

#execute our query and return the data    
def query_db(sql):
#we're currently limiting the return to 1000 rows
    cursor.execute(sql + ' limit 1000')
    formatted_data = []
#we'll need the field names for headings in the json
    cols = [ d[0] for d in cursor.description ]
    data = cursor.fetchall()
    for row in data:
        cleaned_row = [clean_data(item) for item in row]
        formatted_data.append(cleaned_row)
    return { 'headings': cols, 'data': formatted_data }


#our very simplistic routing
#right now, we're just grabbing everything after dashboard/
#which is the home directory of the app

@app.route('/<query>')
def make_index(query=None):
#this will hold the data we're returning

    data = {}
    params = make_params(query)
#map the data type requested to the actual table name
    tables = {'voter': 'nc_voters_new',
                'health': 'rr',
                'property-Buncombe': 'dash_buncombe_property',
                'realestate-Buncombe': 'dash_buncombe_real_estate',
                'property-New Hanover': 'dash_nh_property',
                'realestate-New Hanover': 'dash_nh_real_estate',
                'property-Wake': 'dash_buncombe_property',
                'realestate-Wake': 'dash_wake_real_estate',
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
                table_key = '-'.join([data_type,params['county']])
            else:
                table_key = data_type
            data[data_type] = build_query(tables[table_key], params)
#return the json object
    return jsonify(results=data)

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

#we have debugging on for now    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
