use crime;
truncate dash_buncombe_property;
load data local infile '/home/vaughn.hagerty/dash/buncombe/property/WebPrcls.txt' into table dash_buncombe_property fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

