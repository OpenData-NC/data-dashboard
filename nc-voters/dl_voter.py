#!/usr/bin/env python

from subprocess import call

url = 'ftp://alt.ncsbe.gov/data/'
home_dir = '/home/vaughn.hagerty/nc-voters/'
output_zip_dir = home_dir + 'raw/'
output_txt_dir = home_dir + 'txt/'
processed_dir = home_dir + 'processed/'
user = {'user': 'crimeloader','pw':'redaolemirc'}
db = 'crime'
table = 'nc_voters'


def process(txt_file):
    print txt_file
    skip = True
    holder = ''
    processed_file = processed_dir + txt_file
    data_file = output_txt_dir + txt_file
    with open(data_file, 'r') as voter_file, open(processed_file, 'w') as finished:
        for line in voter_file:
            if skip:
                skip = False
                continue
#            line = line.replace('"','')
            pieces = line.split("\"\t\"")
            stripped = [piece.strip(' "\t\n\r') for piece in pieces]
            stripped[24] = stripped[24].replace(' ','')
            stripped[31] = make_date(stripped[31])
            finished.write("\t".join(stripped) + "\n")
        voter_file.close()
        finished.close()
    load(db,processed_file,table,user)

	
def load(database,data_file, table, user):
    load_command = 'mysql --local-infile --user=' + user['user'] + ' --password=' + user['pw'] + ' ' + database + ' -e '\
    + '"ALTER TABLE ' +  table + ' DISABLE KEYS;SET bulk_insert_buffer_size=1024*1024*256;load data local infile \'' + data_file + '\' '\
    + 'into table ' + table + ';"'
    call(load_command,shell=True)

	
def dl(zip_file):
    output_zip_filename = output_zip_dir + zip_file
    dl_command = 'wget -N -q -O ' + output_zip_filename + ' ' + url + zip_file
    unzip_command = 'unzip -q -o ' + output_zip_filename + ' -d ' + output_txt_dir
    call(dl_command,shell=True)
    call(unzip_command,shell=True)
    process(zip_file.replace('zip','txt'))

	
def make_date(date):
#doing it this way because sboe has some dates < 1900 ... go figure ...
    pieces = date.split('/')
    if len(pieces) < 3:
        return ''
    return pieces[2] + '/' + pieces[0] + '/' + pieces[1]


def main():    
    for i in range(1,101):
        zip_file = 'ncvoter' + str(i) + '.zip'
        dl(zip_file)
if __name__ == "__main__":
    main()
