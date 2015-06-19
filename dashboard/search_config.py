all_search_items = {
    'incidents': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                  'county': 'county = "%s"', 'from-date': 'reported_date = "%s"',
                  'to-date': '(reported_date >= "%s" and reported_date <= "%s")',
                  'street-number': 'address like "%s %%"',
                  'street-name': 'address like "%%%s%%"', 'category-type': 'category in (%s)', 
                  'gender-type': 'sex in (%s)', 'min-age': 'age >= %s', 'max-age': 'age <= %s',
                  'record_id':'record_id = "%s"','agency': 'agency = "%s"',
                  'last-searched': 'added >= "%s"'
                  },
    'arrests': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                  'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                  'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                  'street-number': 'address like "%s %%"',
                  'street-name': 'address like "%%%s%%"', 'category-type': 'category in (%s)', 
                  'gender-type': 'sex in (%s)', 'min-age': 'age >= %s', 'max-age': 'age <= %s',
                  'record_id':'record_id = "%s"','agency': 'agency = "%s"',
                  'last-searched': 'added >= "%s"'},
    'citations': {'first-name': 'name like "%% %s%%"', 'last-name': 'name like "%s,%%"',
                  'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                  'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                  'street-number': 'address like "%s %%"',
                  'street-name': 'address like "%%%s%%"', 
                  'gender-type': 'sex in (%s)', 'min-age': 'age >= %s', 'max-age': 'age <= %s',
                  'record_id':'record_id = "%s"','agency': 'agency = "%s"',
                  'last-searched': 'added >= "%s"'},
    'accidents': {'first-name': '(name1 like "%s%%" or name2 like "%s%%")',
                  'last-name': '(name1 like "%% %s" or name2 like "%% %s")',
                  'county': 'county = "%s"', 'from-date': 'date_occurred = "%s"',
                  'to-date': '(date_occurred >= "%s" and date_occurred <= "%s")',
                  'street-number': 'address like "%s %%"',
                  'street-name': 'address like "%%%s%%"',
                  'record_id':'record_id = "%s"','agency': 'agency = "%s"',
                  'last-searched': 'added >= "%s"'},
    'nc_voters_new': {'ncid': 'ncid = "%s"', 'first-name': 'first_name like "%s%%"',
                  'last-name': 'last_name = "%s"',
                  'county': 'county_desc = "%s"',
                  'street-number': 'res_street_address like "%s %%"',
                  'street-name': 'res_street_address like "%%%s%%"', 'city': 'res_city_desc = "%s"',
                  'party-type': 'party_cd in (%s)', 'gender-type': 'gender_code in (%s)'},
    'rr': {'facility_id': 'facility_id = "%s"', 'first-name': 'fac_name like "%%%s%%"', 'last-name': 'fac_name like "%s%%"',
                  'location-name': 'fac_name like "%%%s%%"', 'county': 'county = "%s"', 'from-date': 'activity_date = "%s"',
                  'to-date': '(activity_date >= "%s" and activity_date <= "%s")',
                  'street-number': 'addr_line1 like "%s %%"',
                  'street-name': 'addr_line1 like "%%%s%%"', 'city': 'addr_city = "%s"', 'zip-code': 'addr_zip5 = "%s"'},
    'dash_nh_rr': {'facility_id': 'facility_id = "%s"', 'first-name': 'fac_name like "%%%s%%"', 'last-name': 'fac_name like "%s%%"',
                  'location-name': 'fac_name like "%%%s%%"', 'county': 'county = "%s"', 'from-date': 'activity_date = "%s"',
                  'to-date': '(activity_date >= "%s" and activity_date <= "%s")',
                  'street-number': 'addr_line1 like "%s %%"',
                  'street-name': 'addr_line1 like "%%%s%%"', 'city': 'addr_city = "%s"', 'zip-code': 'addr_zip5 = "%s"'},
    'dash_buncombe_property': {'parcelid': 'parcelid = "%s"', 'first-name': '(owner1_firstname like "%s%%" or owner2_firstname like "%s%%")',
                  'last-name': '(owner1_lastname = "%s" or owner2_lastname = "%s")',
                  'from-date': 'deeddate = "%s"',
                  'to-date': '(deeddate >= "%s" and deeddate <= "%s")',
                  'street-number': 'housenum = "%s"',
                  'street-name': 'streetname = "%s"', 'min-value': 'taxableVal >= %s', 'max-value': 'taxableVal <= %s'},
    'dash_buncombe_real_estate': {'parcelid': 'parcelid = "%s"', 'first-name': '(seller1_fname like "%s%%" or seller2_fname like "%s%%" or buyer1_fname like "%s%%" or buyer2_fname like "%s%%")',
                  'last-name': '(seller1_lname = "%s" or seller2_lname = "%s" or buyer1_lname = "%s" or buyer2_lname = "%s")',
                  'buyer-first-name': '(buyer1_fname like "%s%%" or buyer2_fname like "%s%%")', 'buyer-last-name': '(buyer1_lname = "%s" or buyer2_lname = "%s")',
                  'seller-first-name': '(seller1_fname like "%s%%" or seller2_fname like "%s%%")', 'seller-last-name': '(seller1_lname = "%s" or seller2_lname = "%s")',                      
                  'from-date': 'selldate = "%s"',
                  'to-date': '(selldate >= "%s" and selldate <= "%s")',
                  'street-number': 'housenum = "%s"',
                  'street-name': 'streetname = "%s"','min-value': 'sellingPrice >= %s', 'max-value': 'sellingPrice <= %s'},

    'dash_nh_property': {'pid': 'pid = "%s"', 'first-name': '(owner like "%%%s%%" or `co-owner` like "%%%s%%")',
                  'last-name': '(owner like "%s%%" or `co-owner` like "%s%%")',
                  'street-number': '`situs-num` like "%%%s"',
                  'street-name': '`situs-street` like "%s%%"', 'min-value': '`real-assval` >= %s', 'max-value': '`reall-assval` <= %s'},

    'dash_nh_real_estate': {'pid': 'pid = "%s"', 'instrument': 'instrument = "%s"', 'buyer': 'buyer = "%s"', 'seller': 'seller = "%s"', 'first-name': '(seller like "%s%%" or buyer like "%s%%")',
                  'last-name': '(seller like "%% %s" or buyer like "%% %s")',
                  'buyer-first-name': 'buyer like "%%%s%%"', 'buyer-last-name': 'buyer like "%%%s%%"',
                  'seller-first-name': 'seller like "%%%s%%"', 'seller-last-name': 'seller like "%%%s%%"',                      
                  'from-date': 'sale_date = "%s"',
                  'to-date': '(sale_date >= "%s" and sale_date <= "%s")',
                  'street-number': 'address like "%s %%"',
                  'street-name': 'address like "%%%s%%"', 'min-value': 'price >= %s', 'max-value': 'price <= %s'},

    'dash_wake_property': {'pin_num': 'pin_num = "%s"', 'card_number': 'card_number = "%s"', 'first-name': '(owner_line1 like "%s%%" or owner_line2 like "%s%%")',
                  'last-name': '(owner_line1 like "%% %s" or owner_line1 like "%% %s")',
                  'from-date': 'total_sale_date = "%s"',
                  'to-date': '(total_sale_date >= "%s" and total_sale_date <= "%s")',
                  'street-number': 'site_address_street_number = "%s"',
                  'street-name': 'site_address_street_name = "%s"', 'min-value': 'sum(building_assessed_value,land_assessed_value) >= %s', 'max-value': 'sum(building_assessed_value,land_assessed_value) <= %s'},

    'dash_wake_real_estate': {'pin_num': 'pin_num = "%s"', 'card_number': 'card_number = "%s"', 'first-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%")',
                  'last-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%")',
                  'buyer-first-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%")', 'buyer-last-name': '(buyer_line1 like "%%%s%%" or buyer_line2 like "%%%s%%")',
                  'seller-first-name': '', 'seller-last-name': '',     #no seller data in wake                 
                  'from-date': 'total_sale_date = "%s"',
                  'to-date': '(total_sale_date >= "%s" and total_sale_date <= "%s")',
                  'street-number': 'site_address_street_number = " %s"',
                  'street-name': 'site_address_street_name = " %s"', 'min-value': 'total_sale_price >= %s', 'max-value': 'total_sale_price <= %s'}
}
#fields we're selecting for return for each table
selects = {
    'incidents': 'concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_reported,"%%m/%%d/%%Y") `Date reported` , category `Category`, incidents.charge `Charge`, address `Address`, if(pdf="" or pdf is null, "N/A", pdf) `View report`',
    'arrests': 'concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%%m/%%d/%%Y") `Date occurred`, `Category`, arrests.charge `Charge`, address `Address`, if(pdf="" or pdf is null, "N/A", pdf) `View report`',
    'citations': 'concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%%m/%%d/%%Y") `Date occurred`, charge, address `Address`',
    'accidents': 'concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name1 `Driver 1`, name2 `Driver 2`, date_format(date_occurred,"%%m/%%d/%%Y") `Date occurred`, address `Address`, if(pdf="" or pdf is null, "N/A", pdf) `View report`',
    'nc_voters_new': 'concat_ws("|", "ncid", ncid) `Record ID`, voter_reg_num `Voter reg. num.`, first_name `First name`, last_name `Last name`, res_street_address `Address` , res_city_desc `City`, zip_code `Zip code`',
    'rr': 'concat_ws("|","facility_id",facility_id,"from-date",activity_date) `Record ID`, fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%%m/%%d/%%Y") `Insp. date`, activity_final_score `Score`',
    'dash_buncombe_property': 'concat_ws("|","parcelid",parcelid) `Record ID`, parcelid `Parcel ID`, concat_ws(" ", owner1_firstname, owner1_lastname) `Owner 1`, concat_ws(" ", owner2_firstname, owner2_lastname) `Owner 2`, date_format(deeddate,"%%m/%%d/%%Y") `Deed date`, concat_ws(" ", housenum, housesuffix, streetdirection, streetname, streettype) `address`, citycode `City code`, taxableval `Tax value`',
    'dash_buncombe_real_estate': 'concat_ws("|","parcelid",parcelid,"from-date",selldate) `Record ID`, parcelid `Parcel ID`, concat_ws(" ", seller1_fname, seller1_lname) `Seller 1`, concat_ws(" ", seller2_fname, seller2_lname) `Seller 2`, concat_ws(" ", buyer1_fname, buyer1_lname) `Buyer 1`, concat_ws(" ", buyer2_fname, buyer2_lname) `Buyer 2`,date_format(selldate,"%%m/%%d/%%Y") `Sale date`, concat_ws(" ", housenum, housesuffix, streetdirection, streetname, streettype) `address`, citycode `City code`, sellingprice `Sale price`',
    'dash_nh_property': 'concat_ws("|", "pid", pid) `Record ID`, pid `Parcel ID`, owner `Owner 1`, `co-owner` `Owner 2`, concat_ws(" ", `situs-num`, `situs-street`) `Address`, `situs-city` `City code`, `real-assval` `Tax value`',
    'dash_nh_real_estate': 'concat_ws("|", "pid", pid, "from-date", sale_date, "instrument", instrument, "buyer", buyer, "seller", seller) `Record ID`, pid `Parcel ID`, seller `Seller`, buyer `Buyer`, date_format(sale_date,"%%m/%%d/%%Y") `Sale date`, address `Address`, city `City`, price `Sale price`',
    'dash_wake_property': 'concat_ws("|", "pin_num", pin_num, "card_number", card_number, "from-date",total_sale_date) `Record ID`, pin_num `Parcel ID`, owner_line1 `Owner 1`, owner_line2 `Owner 2`, date_format(deed_date,"%%m/%%d/%%Y") `Deed date`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `address`, city `City code`, sum(building_assessed_value,land_assessed_value) `Tax value`',
    'dash_wake_real_estate': 'concat_ws("|", "pin_num", pin_num, "card_number", card_number) `Record ID`, pin_num `Parcel ID`, buyer_line1 `Buyer 1`, buyer_line2 `Buyer 2`, date_format(total_sale_date,"%%m/%%d/%%Y") `Sale date`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `address`, city `City code`, total_sale_price `Sale price`'
#        'nc_voters': 'voter_reg_num `Voter reg. num.`, first_name `First name`, last_name `Last name`, res_street_address `Address` , res_city_desc `City`, zip_code `Zip code`, full_phone_number `Phone num.`',
}

# selects used for individual record detail displays
detail_selects = {
    'incidents': 'if(id_generate=1,"N/A",record_id) as record_id, agency, name, if(age=0,"",age) as age, race, sex, if(date(on_date) = "0000-00-00", concat_ws(" ", "Between",date_format(from_date,"%%m/%%d/%%Y %%h:%%i %%p"),"and",date_format(to_date,"%%m/%%d/%%Y %%h:%%i %%p")), date_format(on_date,"%%m/%%d/%%Y %%h:%%i %%p")) as date_occurred, date_format(date_reported,"%%m/%%d/%%Y %%h:%%i %%p") as date_reported, address, incidents.charge as charge, category, offense_code, reporting_officer, replace(pdf,"/home/vaughn.hagerty/crime-scrapers","http://pdf.open-nc.org") as pdf',
    'arrests' : 'if(id_generate=1,"N/A",record_id) as record_id, agency, name, if(age=0,"",age) as age, race, sex, date_format(date_occurred,"%%m/%%d/%%Y %%h:%%i %%p") as date_occurred, address, arrests.charge, category, offense_code, reporting_officer, replace(pdf,"/home/vaughn.hagerty/crime-scrapers","http://pdf.open-nc.org") as pdf',
    'citations': 'if(id_generate=1,"N/A",record_id) as record_id, agency, name, if(age=0,"",age) as age, race, sex, date_format(date_occurred,"%%m/%%d/%%Y %%h:%%i %%p") as date_occurred, address, charge',
    'accidents' : 'if(id_generate=1,"N/A",record_id) as record_id, agency, name1, name2, date_format(date_occurred,"%%m/%%d/%%Y %%h:%%i %%p") as date_occurred, address, reporting_officer, replace(pdf,"/home/vaughn.hagerty/crime-scrapers","http://pdf.open-nc.org") as pdf',
    'rr': 'fac_name, addr_line1, addr_city, addr_zip5, date_format(activity_date, "%%m/%%d/%%Y") as activity_date, activity_final_score, replace(item_comments,";","<p>") as item_comments',
    'dash_nh_rr': 'fac_name, addr_line1, addr_city, addr_zip5, date_format(activity_date, "%%m/%%d/%%Y") as activity_date, activity_final_score, replace(item_comments,";","<p>") as item_comments',
    'nc_voters_new':'concat_ws(" ",if(length(trim(name_prefx_cd)), trim(name_prefx_cd), NULL), if(length(trim(first_name)), trim(first_name), NULL), if(length(trim(midl_name)), trim(midl_name), NULL), if(length(trim(last_name)), trim(last_name), NULL), if(length(trim(name_sufx_cd)), trim(name_sufx_cd), NULL) ) as name, res_street_address, res_city_desc, state_cd res_state_cd, zip_code res_zip_code, concat_ws(", ", if(length(trim(mail_addr1)), trim(mail_addr1), NULL), if(length(trim(mail_addr2)), trim(mail_addr2), NULL), if(length(trim(mail_addr3)), trim(mail_addr3), NULL), if(length(trim(mail_addr4)), trim(mail_addr4), NULL) ) as mail_addr, mail_city, mail_state, mail_zipcode, full_phone_number, race_code, ethnic_code, party_cd, gender_code, birth_age, birth_place, drivers_lic, date_format(registr_dt, "%%m/%%d/%%Y") as registr_dt, voter_reg_num, voter_status_desc, voter_status_reason_desc, absent_ind, party_cd, precinct_desc, municipality_desc, ward_desc, cong_dist_abbrv, super_court_abbrv, judic_dist_abbrv, nc_senate_abbrv, nc_house_abbrv, county_commiss_desc, township_desc, school_dist_desc, fire_dist_desc, water_dist_desc, sewer_dist_desc, sanit_dist_desc, rescue_dist_desc, munic_dist_desc, dist_1_desc, dist_2_desc, vtd_desc',
    'dash_nh_property': '*',
    'dash_nh_real_estate': '*',
    'dash_buncombe_property': '*',
    'dash_buncombe_real_estate': '*',
    'dash_wake_property': '*',
    'dash_wake_real_estate': '*',

}

#any joins we might need, such as county name lookups and crime categories

joins = {
    'incidents': ' inner join charge_categories on incidents.charge = charge_categories.charge',
    'arrests': ' inner join charge_categories on arrests.charge = charge_categories.charge',
    'citations': '',
    'accidents': '',
    'nc_voters_new': '',
    'rr': ' inner join rr_counties on county_id = c_id ',
    'dash_nh_rr': ' inner join rr_counties on county_id = c_id ',
    'dash_buncombe_property': '',
    'dash_buncombe_real_estate': '',
    'dash_nh_property': '',
    'dash_nh_real_estate': '',
    'dash_wake_property': '',
    'dash_wake_real_estate': ''
    
}

#orders and limits, used for detail searches

order_limit = {
    'rr': ' order by activity_date desc limit 1',
    'dash_nh_rr': ' order by activity_date desc limit 1'
}


#dictionaries to make the query building below easier
skip_params = ['from-date','to-date','data_types']
#these tables don't have a date field
skip_dates = ['nc_voters_new','dash_nh_property']
#some tables have numerous name fields, so we have to account for that when building our query. 
#The number is how many times in addition to the first that we'll use a name string in building a query (e.g. 1 = 2 times, 3 = 4, etc.)
#name_counts = {'accidents': 1, 'dash_buncombe_property': 1, 'dash_buncombe_real_estate': 3,'dash_nh_property': 1, 'dash_nh_real_estate': 1,'dash_wake_property': 1, 'dash_wake_real_estate': 1 }
name_counts = {
    'accidents': {'first-name':1, 'last-name': 1},
    'dash_buncombe_property': {'first-name':1, 'last-name': 1}, 
    'dash_buncombe_real_estate': {'first-name':3, 'last-name': 3, 'buyer-first-name': 1, 'buyer-last-name': 1,
    'seller-first-name': 1, 'seller-last-name': 1},
    'dash_nh_property': {'first-name':1, 'last-name': 1}, 
    'dash_nh_real_estate': {'first-name':1, 'last-name': 1},
    'dash_wake_property': {'first-name':1, 'last-name': 1 }, 
    'dash_wake_real_estate': {'first-name':1, 'last-name': 1, 'buyer-first-name':1, 'buyer-last-name': 1 }
}
#we don't use the county in these tables. they don't have a county field because they're already county-specific.
skip_counties = ['dash_buncombe_property','dash_buncombe_real_estate','dash_nh_property', 'dash_nh_real_estate','dash_wake_property', 'dash_wake_real_estate']
#no seller data in wake
skip_sellers = ['dash_wake_real_estate']
#the query for these needs to use in (val1, val2)
in_categories = ['category-type', 'party-type', 'gender-type']
