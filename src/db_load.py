from subprocess import call
def load(database,data_file, table, user):
	all_fields = {
		'incidents': '(record_id, agency, name, age, race, sex, on_date, from_date, to_date,reported_date, date_reported, time_reported, address, charge, offense_code, reporting_officer,pdf, street_address, city, county, state, zip, lat, lon, scrape_type, id_generate)',
		'arrests': '(record_id, agency, name, age, race, sex, occurred_date, date_occurred, time_occurred, address, charge, offense_code, reporting_officer,pdf, street_address, city, county, state, zip, lat, lon, scrape_type, id_generate)',
		'citations': '(record_id, agency, name, age, race, sex, occurred_date, date_occurred, time_occurred, reporting_officer,pdf, street_address, city, county, state, zip, lat, lon, scrape_type, id_generate)',
		'accidents': '(record_id, agency, name1, name2, occurred_date, date_occurred, time_occurred, address, reporting_officer,pdf, street_address, city, county, state, zip, lat, lon, scrape_type, id_generate)'
	}
	data_type = table.lower()
	fields = ' ' + all_fields[data_type]

	load_command = 'mysql --local-infile --user=' + user['user'] + ' --password=' + user['pw'] + ' ' + database + ' -e '\
	+ '"load data local infile \'' + data_file + '\' '\
	+ 'replace into table ' + table.lower() + fields + '";'
	call(load_command,shell=True)

