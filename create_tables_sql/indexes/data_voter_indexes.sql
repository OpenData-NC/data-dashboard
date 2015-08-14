alter table nc_voters_new add index(county_desc, last_name, first_name);
alter table nc_voters_new add index(county_desc, res_street_address, res_city, zip_code);
alter table nc_voters_new add index(county_desc,registr_dt);
alter table nc_voters_new add index(county_desc, race_code);
alter table nc_voters_new add index(county_desc, ethnic_code);
alter table nc_voters_new add index(county_desc, gender_code);
alter table nc_voters_new add index(county_desc, party_cd);

