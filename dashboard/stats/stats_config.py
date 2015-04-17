# counties = ['Buncombe', 'New Hanover', 'Wake']
counties = {
            'Buncombe': ['incidents','arrests','accidents','citations','dash_buncombe_real_estate','rr','nc_voters_new'], 
            'New Hanover': ['incidents','arrests','accidents','citations','dash_nh_real_estate','dash_nh_rr','nc_voters_new'],
            'Wake':['incidents','arrests','accidents','citations','dash_wake_real_estate','rr','nc_voters_new'],
}

data_types = {
                'incidents': ['all', 'by category', 'by day of week', 'by officer'],
                'arrests': ['all', 'by category', 'by day of week', 'by officer'],
                'accidents': ['all', 'by day of week', 'by officer'],
                'citations': ['all', 'by day of week'],
                'dash_buncombe_real_estate': ['all', 'total by day', 'top 10 sellers', 'top 10 buyers'],
                'dash_nh_real_estate': ['all', 'total by day', 'top 10 sellers', 'top 10 buyers'],
                'dash_wake_real_estate': ['all', 'total by day', 'top 10 buyers'],
                'rr': ['all', 'lowest 10 scores', 'score distribution'],
                'dash_nh_rr': ['all', 'lowest 10 scores', 'score distribution'],
#                'nc_voters_new': ['by party', 'party by precinct'],
                'nc_voters_new': ['by party'],
}

no_county = ['dash_buncombe_real_estate','dash_nh_real_estate', 'dash_wake_real_estate']

date_fields = {
                'incidents': 'date_reported',
                'arrests': 'date_occurred',
                'accidents': 'date_occurred',
                'citations': 'date_occurred',
                'dash_buncombe_property': 'deeddate',
                'dash_buncombe_real_estate': 'selldate',
                'dash_nh_real_estate': 'sale_date',
                'dash_wake_property': 'total_sale_date',
                'dash_wake_real_estate': 'total_sale_date',
                'rr': 'activity_date',
                'dash_nh_rr': 'activity_date',
            }



#note that this might not return incidents or arrests without categories
joins = {
        'rr': ' inner join rr_counties on county_id = c_id ',
        'dash_nh_rr': ' inner join rr_counties on county_id = c_id ',
        'incidents': ' left join charge_categories on incidents.charge = charge_categories.charge ',
        'arrests': ' left join charge_categories on arrests.charge = charge_categories.charge ',
        'dash_buncombe_real_estate': ' left join dash_buncombe_addresses on full_address = concat_ws(" ", if(length(trim(housenum)), trim(housenum), NULL), if(length(trim(housesuffix)), trim(housesuffix), NULL), if(length(trim(streetdirection)), trim(streetdirection), NULL), if(length(trim(streetname)), trim(streetname), NULL), if(length(trim(streettype)), trim(streettype), NULL)) ',
        'dash_nh_real_estate': ' ',
#        'dash_wake_real_estate': ' left join dash_wake_addresses on pin_num = pin ',
}

select_all = {
        'incidents': {
            'all': ' concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_reported,"%m/%d/%Y") `Date reported` , if(category is null, "Uncategorized", category) `Category`, incidents.charge `Charge`, address `Address`, lat, lon ',
            'by category': '  category `Category`, count(*) `Count` ',
            'by day of week': ' dayofweek(date_reported) `Order`, date_format(date_reported,"%W") `Day`, count(*) `Count` ',
            'by hour of day': ' hour(reported_date) `Hour`, count(*) `Count` ', #note that might be problem with those without hours
            'by address': ' address `Address`, count(*) `Count` ', #note that might need to filter out '', restricted etc.
            'by officer': ' agency `Source agency`, reporting_officer `Reporting officer`, count(*) `Count` ',
        },
        'arrests': {
            'all': ' concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, if(category is null, "Uncategorized", category) `Category`, arrests.charge `Charge`, address `Address`, lat, lon ',
            'by category': '  category `Category`, count(*) `Count` ',
            'by day of week': ' dayofweek(date_occurred) `Order`, date_format(date_occurred,"%W") `Day`, count(*) `Count` ',
            'by hour of day': ' hour(occurred_date) `Hour`, count(*) `Count` ', #note that might be problem with those without hours
            'by address': ' address `Address`, count(*) `Count` ', #note that might need to filter out '', restricted etc.
            'by officer': ' agency `Source agency`, reporting_officer `Reporting officer`, count(*) `Count` ',
        },
        'accidents': {
            'all': ' concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name1 `Driver 1`, name2 `Driver 2`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, address `Address` ',
            'by day of week': ' dayofweek(date_occurred) `Order`, date_format(date_occurred,"%W") `Day`, count(*) `Count` ',
            'by address': ' address `Address`, count(*) `Count` ', #note that might need to filter out '', restricted etc.
            'by officer': ' agency `Source agency`, reporting_officer `Reporting officer`, count(*) `Count` ',
        
        },
        'citations': {
            'all': ' concat_ws("|", "record_id", record_id, "agency", agency) `Record ID`, agency `Agency`, name `Name`, date_format(date_occurred,"%m/%d/%Y") `Date occurred`, charge, address `Address` ',
            'by day of week': ' dayofweek(date_occurred) `Order`, date_format(date_occurred,"%W") `Day`, count(*) `Count` ',
            'by address': ' address `Address`, count(*) `Count` ', #note that might need to filter out '', restricted etc.
            'by officer': ' agency `Source agency`, reporting_officer `Reporting officer`, count(*) `Count` ',
        
        },
        'rr': {
            'all': ' concat_ws("|","facility_id",facility_id,"from-date",activity_date) `Record ID`, fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%m/%d/%Y") `Insp. date`, activity_final_score `Score` ',
            'lowest 10 scores': ' concat_ws("|","facility_id",facility_id,"from-date",activity_date) `Record ID`, fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%m/%d/%Y") `Insp. date`, activity_final_score `Score` ',
            'score distribution': ' activity_final_score `Score`, count(activity_final_score) as `Count` ',
        
        },
        'dash_nh_rr': {
            'all': ' concat_ws("|","facility_id",facility_id,"from-date",activity_date) `Record ID`, fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%m/%d/%Y") `Insp. date`, activity_final_score `Score` ',
            'lowest 10 scores': ' concat_ws("|","facility_id",facility_id,"from-date",activity_date) `Record ID`, fac_name `Facility name`, addr_line1 `Address`, addr_city `City`, addr_zip5 `ZIP code`,date_format(activity_date,"%m/%d/%Y") `Insp. date`, activity_final_score `Score` ',
            'score distribution': ' activity_final_score `Score`, count(activity_final_score) as `Count` ',
        
        },
        'nc_voters_new': {
            'by party': ' party_cd `Party`, count(*) `Count` ',
            'party by precinct': ' precinct_desc `Precinct`, party_cd `Party`, count(*) `Count` ',
        
        },
        'dash_buncombe_property': {
            'none': '',
        },
        'dash_buncombe_real_estate': {
            'all': ' concat_ws("|","parcelid",parcelid,"from-date",selldate) `Record ID`, date_format(selldate, "%m/%d/%Y") `Sale date`, concat(seller1_fname," ", seller1_lname) `Seller 1`,concat(seller2_fname," ", seller2_lname) `Seller 2`, concat(buyer1_fname," ", buyer1_lname) `Buyer 1`, concat(buyer2_fname," ", buyer2_lname) `Buyer 2`, concat_ws(" ", if(length(trim(housenum)), trim(housenum), NULL), if(length(trim(housesuffix)), trim(housesuffix), NULL), if(length(trim(streetdirection)), trim(streetdirection), NULL), if(length(trim(streetname)), trim(streetname), NULL), if(length(trim(streettype)), trim(streettype), NULL)) `Address`, citycode `City code`, sellingprice `Sale price`, lat, lon ',
            'total by day': '  date_format(selldate,"%m/%d/%Y") `Sale date`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
            'top 10 sellers': '  concat_ws(" ",seller1_fname, seller1_lname, seller2_fname, seller2_lname) `Sellers`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
            'top 10 buyers': ' concat_ws(" ",buyer1_fname, buyer1_lname, buyer2_fname, buyer2_lname) `Buyers`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
        },
        # 'dash_buncombe_real_estate': {
            # 'all': ' parcelid `Parcel ID`, date_format(selldate, "%m/%d/%Y") `Sale date`, concat(seller1_fname," ", seller1_lname) `Seller 1`,concat(seller2_fname," ", seller2_lname) `Seller 2`, concat(buyer1_fname," ", buyer1_lname) `Buyer 1`, concat(buyer2_fname," ", buyer2_lname) `Buyer 2`, concat_ws(" ", if(length(trim(housenum)), trim(housenum), NULL), if(length(trim(housesuffix)), trim(housesuffix), NULL), if(length(trim(streetdirection)), trim(streetdirection), NULL), if(length(trim(streetname)), trim(streetname), NULL), if(length(trim(streettype)), trim(streettype), NULL)) `Address`, citycode `City code`, sellingprice `Sale price`, lat, lon ',
            # 'total by day': '  date_format(selldate,"%m/%d/%Y") `Sale date`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
            # 'top 10 sellers': '  concat_ws(" ",seller1_fname, seller1_lname, seller2_fname, seller2_lname) `Sellers`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
            # 'top 10 buyers': ' concat_ws(" ",buyer1_fname, buyer1_lname, buyer2_fname, buyer2_lname) `Buyers`, sum(sellingprice) `Total $s sold`, count(*) `Count` ',
        # },
        'dash_nh_property': {
            'none': '',
        
        },
        # 'dash_nh_real_estate': {
            # 'all': ' concat_ws("|","pid",pid,"from-date",sale_date) `Record ID`, date_format(sale_date,"%m/%d/%Y") `Sale date`, seller `Seller`, buyer `Buyer`, address `Address`, city `City`, price `Sale price` ',
            # 'total by day': ' date_format(sale_date, "%m/%d/%Y") `Sale date`, sum(price) `Total $s sold`, count(*) `Count` ',
            # 'top 10 sellers': ' seller `Sellers`, sum(price) `Total $s sold`, count(*) `Count` ',
            # 'top 10 buyers': ' buyer `Buyers`, sum(price) `Total $s sold`, count(*) `Count` ',
        # },
        'dash_nh_real_estate': {
            'all': ' concat_ws("|", "pid", pid, "from-date", sale_date, "instrument", instrument, "buyer", buyer, "seller", seller) `Record ID`, pid `Parcel ID`, date_format(sale_date,"%m/%d/%Y") `Sale date`, seller `Seller`, buyer `Buyer`, address `Address`, city `City`, price `Sale price` ',
            'total by day': ' date_format(sale_date, "%m/%d/%Y") `Sale date`, sum(price) `Total $s sold`, count(*) `Count` ',
            'top 10 sellers': ' seller `Sellers`, sum(price) `Total $s sold`, count(*) `Count` ',
            'top 10 buyers': ' buyer `Buyers`, sum(price) `Total $s sold`, count(*) `Count` ',
        },
        'dash_wake_property': {
            'none': '',
        },
        # 'dash_wake_real_estate': {
            # 'all': ' concat_ws("|","pin_num",pin_num,"from-date",total_sale_date) `Record ID`, date_format(total_sale_date,"%m/%d/%Y") `Sale date`, seller_line1 `Seller 1`,seller_line2 `Seller 2`, buyer_line1 `Buyer 1`, buyer_line2 `Buyer 2`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `Address`, dash_wake_real_estate.city `City code`, total_sale_price `Sale price` ',
            # 'total by day': ' date_format(total_sale_date,"%m/%d/%Y") `Sale date`, sum(total_sale_price) `Total $s sold`, count(*) `Count` ',
# #            'top 10 sellers': '', 
# #wake doesn't have right now
            # 'top 10 buyers': ' concat_ws(" ",buyer_line1, buyer_line2) `Buyers`, sum(total_sale_price)`Total $s sold`, count(*) `Count` ',
        # },
        'dash_wake_real_estate': {
            'all': ' concat_ws("|", "pin_num", pin_num, "card_number", card_number, "from-date",total_sale_date) `Record ID`, pin_num `PIN`, date_format(total_sale_date,"%m/%d/%Y") `Sale date`, seller_line1 `Seller 1`,seller_line2 `Seller 2`, buyer_line1 `Buyer 1`, buyer_line2 `Buyer 2`, concat_ws(" ", site_address_street_number, site_address_street_units, site_address_street_prefix, site_address_street_name, site_address_street_type, site_address_street_suffix) `Address`, dash_wake_real_estate.city `City code`, total_sale_price `Sale price` ',
            'total by day': ' date_format(total_sale_date,"%m/%d/%Y") `Sale date`, sum(total_sale_price) `Total $s sold`, count(*) `Count` ',
#            'top 10 sellers': '', 
#wake doesn't have right now
            'top 10 buyers': ' concat_ws(" ",buyer_line1, buyer_line2) `Buyers`, sum(total_sale_price)`Total $s sold`, count(*) `Count` ',
        },

}

groups_orders_limits = {
        'incidents': {
            'all': ' order by `Date reported` desc',
            'by category': ' group by `Category`',
            'by day of week': ' group by `Order` order by `Order`',
            'by hour of day': ' group by `Hour` order by `Hour`',
            'by address': ' and group by `Address` order by `Count` desc limit 10', #note that might need to filter out '', restricted etc.
            'by officer': ' and reporting_officer not in ("&nbsp;","") group by `Reporting officer` order by `Count` desc limit 10',
        },
        'arrests': {
            'all': ' order by `Date occurred` desc',
            'by category': ' group by `Category`',
            'by day of week': ' group by `Order` order by `Order`',
            'by hour of day': ' group by `Hour` order by `Hour`',
            'by address': ' group by `Address` order by `Count` desc limit 10', #note that might need to filter out '', restricted etc.
            'by officer': ' and reporting_officer not in ("&nbsp;","") group by `Reporting officer` order by `Count` desc limit 10',
        },
        'accidents': {
            'all': ' order by `Date occurred` desc',
            'by day of week': ' group by `Order` order by `Order`',
            'by address': ' group by `Address` order by `Count` desc limit 10', #note that might need to filter out '', restricted etc.
            'by officer': ' and reporting_officer not in ("&nbsp;","") group by `Reporting officer` order by `Count` desc limit 10',
        
        },
        'citations': {
            'all': ' order by `Date occurred` desc',
            'by day of week': ' group by `Order` order by `Order`',
            'by address': ' group by `Address` order by `Count` desc limit 10', #note that might need to filter out '', restricted etc.
            'by officer': ' and reporting_officer not in ("&nbsp;","") group by `Reporting officer` order by `Count` desc limit 10',
        
        },
        'rr': {
            'all': ' order by `Facility name`',
            'lowest 10 scores': ' and activity_final_score != "0.0" order by `Score` limit 10',
            'score distribution': ' and activity_final_score != "0.0" group by `Score` order by `Score`',
        },
        'dash_nh_rr': {
            'all': ' order by `Facility name`',
            'lowest 10 scores': ' and activity_final_score != "0.0" order by `Score` limit 10',
            'score distribution': ' and activity_final_score != "0.0" group by `Score` order by `Score`',
        },
        'nc_voters_new': {
            'by party': ' and voter_status_desc in ("ACTIVE","TEMPORARY") group by `Party` order by `Party`',
            'party by precinct': ' and voter_status_desc in ("ACTIVE","TEMPORARY") group by `Precinct`, `Party` order by `Precinct`, `Party`',            
        
        },
        'dash_buncombe_property': {
            'none': '',
        },
        'dash_buncombe_real_estate': {
            'all': ' order by `Sale date` desc',
            'total by day': ' group by `Sale date` order by `Sale date`',
            'top 10 sellers': ' group by `Sellers` order by `Count` desc limit 10',
            'top 10 buyers': ' group by `Buyers` order by `Count` desc limit 10',
        
        },
        'dash_nh_property': {
            'none': '',        
        },
        'dash_nh_real_estate': {
            'all': ' order by `Sale date` desc',
            'total by day': ' group by `Sale date` order by `Sale date`',
            'top 10 sellers': ' group by `Sellers` order by `Count` desc limit 10',
            'top 10 buyers': ' group by `Buyers` order by `Count` desc limit 10',
        },
        'dash_wake_property': {        
            'none': '',
        },
        'dash_wake_real_estate': {
            'all': ' order by `Sale date` desc',
            'total by day': ' group by `Sale date` order by `Sale date`',
#            'top 10 sellers': ' group by `Sellers` order by `Count` desc limit 10',
            'top 10 buyers': ' group by `Buyers` order by `Count` desc limit 10',
        },

}

return_types = {
        'incidents': 'Incidents',
        'arrests': 'Arrests',
        'accidents': 'Traffic accidents',
        'citations': 'Citations',
        'dash_buncombe_property': 'Property tax',
        'dash_buncombe_real_estate': 'Real estate',
        'dash_nnh_property': 'Property tax',
        'dash_nh_real_estate': 'Real estate',
        'dash_wake_property': 'Property tax',
        'dash_wake_real_estate': 'Real estate',
        'rr': 'Health inspection scores',
        'dash_nh_rr': 'Health inspection scores',
        'nc_voters_new': 'Voter registration',
}
