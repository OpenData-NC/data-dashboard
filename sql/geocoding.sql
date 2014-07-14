create table county_centers(
	id int not null primary key auto_increment,
	county_name varchar(100),
	lat float(16,13),
	lon float(16,13),
	min_lat float(16,13),
	min_lon float(16,13),
	max_lat float(16,13),
	max_lon float(16,13),
	index(county_name)
)

create table geocoded_addresses(
	id bigint not null primary key auto_increment,
	county_name varchar(100),
	original_address varchar(250),
	standardized_address varchar(250),
	city varchar(100),
	state varchar(100),
	zip mediumint,
	lat float(16,13),
	lon float(16,13),
	date_added timestamp,
	index(original_address),
	index(county_name),
	index(standardized_address)
) 