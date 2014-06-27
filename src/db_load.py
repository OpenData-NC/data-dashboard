from subprocess import call
def load(database,data_file, table, user):
	load_command = 'mysql --local-infile --user=' + user['user'] + ' --password=' + user['pw'] + ' ' + database + ' -e '\
	+ '"load data local infile \'' + data_file + '\' '\
	+ 'replace into table ' + table.lower() + '";'
	call(load_command,shell=True)

