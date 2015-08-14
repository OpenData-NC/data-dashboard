use crime;
truncate dash_buncombe_real_estate;
load data local infile '/home/vaughn.hagerty/dash/buncombe/realestate/WebSales.txt' into table dash_buncombe_real_estate fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

