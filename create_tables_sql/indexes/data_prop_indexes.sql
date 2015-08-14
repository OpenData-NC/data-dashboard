alter table dash_buncombe_property add index(deeddate);
alter table dash_buncombe_real_estate add index(selldate);
alter table dash_wake_property add index(total_sale_date);
alter table dash_wake_real_estate add index (total_sale_date);
alter table dash_buncombe_property add index (owner1_lastname, owner2_lastname,owner1_firstname, owner2_firstname, deeddate, streetname, housenum);
alter table dash_buncombe_real_estate add index (seller1_lname, seller2_lname,seller1_fname, seller2_fname, buyer1_lname, buyer2_lname,buyer1_fname, buyer2_fname, selldate, streetname, housenum);
alter table dash_nh_property add index(owner,`co-owner`,`situs-num`, `situs-street`);
alter table dash_nh_real_estate add index(buyer, seller, sale_date, address);
alter table dash_wake_property add index(owner_line1, owner_line2, total_sale_date, site_address_street_number, site_address_street_name);
alter table dash_wake_real_estate add index(buyer_line1, buyer_line2, total_sale_date, site_address_street_number, site_address_street_name);

