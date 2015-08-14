alter table incidents add index(county,name);
alter table incidents add index(county,date_reported);
alter table incidents add index(county,address);
alter table arrests add index (county,name);
alter table arrests add index(county,date_occurred);
alter table arrests add index(county, address);
alter table accidents add index(county, name1, name2);
alter table accidents add index(county,date_occurred);
alter table accidents add index(county,address);
alter table citations add index(county, name);
alter table citations add index(county, date_occurred);
alter table citations add index(county, address);

