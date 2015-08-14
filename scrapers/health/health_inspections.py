#!/usr/bin/env python
import MySQLdb
import requests
import datetime
import re
from os import path
from subprocess import call

#config stuff
#where we'll store our data
data_dir = '/home/vaughn.hagerty/rr/data/'
#site where state stores its data
url = 'http://ehs.ncpublichealth.com/browsablemedia/'
#used to build path to actual file we want
domain = 'http://ehs.ncpublichealth.com'
#the state apparently has never encountered the concept of a naming convetion.
#as such we can expect a wide variety of names for the data file. when we first hit
#url above, we get a standard Apache-generated directory listing, with the file name
#and creation date. we use that creation date to find our file under the assumption 
#(correct so far) that a file created on the current month and year is the one we want.
#IMPORTANT: We NEVER ran this on a cron because the state could never be relied upon
#for anything. We always did this update at the command line.

#create the pattern we'll use to find our file 
month = datetime.datetime.now().strftime('%m')
date_pattern = datetime.datetime.now().strftime(month.lstrip('0') + '/\d{1,2}/%Y')
pattern = '> +' + date_pattern + '[^"]+"(?P<filename>[^"]+)"'
m = re.compile(pattern)

#we'll use these for database work
user = {'user': [username here], 'pw': [password here]}
table = 'rr'
raw_table = 'rr_raw'
database = 'crime'
connection = MySQLdb.connect(user=user['user'],passwd=user['pw'],db=database)
cursor = connection.cursor()

#grab the file
def fetch_and_format(data_file, target):
    fetch_command = 'wget -q -P ' + data_dir + ' ' + data_file
    call(fetch_command, shell=True)
    #load the data
    load(database, target, raw_table, user)

#load the raw data (not formatted -- e.g., dates) in a table  
def load(database,data_file, table, user):
    load_command = 'mysql --local-infile --user=' + user['user'] + ' --password=' + user['pw'] + ' ' + database + ' -e '\
    + '"truncate ' + table + ';load data local infile \'' + data_file + '\' '\
    + 'into table ' + table.lower() + " fields optionally enclosed by '\\\"'" + " lines terminated by '\\" + "r\\" \
    + "n'" + ' ignore 1 lines";'
    call(load_command,shell=True)

#transfer new records from the raw table into our live table
def insert_data(table, raw_table):
    sql = "SELECT FACILITY_ID_NUMBER, FAC_TYPE, COUNTY_ID, FAC_NAME \
            , ADDR_LINE1, ADDR_CITY, ADDR_ZIP5, ACTIVITY_DATE, STATUS_CODE, ACTIVITY_SCORE \
            , ACTIVITY_FINAL_SCORE, ACTIVITY_GENERAL_COMMENT, ITEM_COMMENTS from %s" % (raw_table)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        row = list(row)
        row[7] = datetime.datetime.strptime(row[7], '%d-%b-%y').strftime('%Y/%m/%d')
        check_sql = 'select * from ' + table + ' where facility_id = "' + row[0] + '" and activity_date = "' + row[7] + '"'
        cursor.execute(check_sql)
        found = cursor.fetchall()
        if not len(found):
            row = [MySQLdb.escape_string(field) for field in row]
            values = '("' + '","'.join(row) + '")'
            insert_sql = 'insert into ' + table + ' values ' + values
            cursor.execute(insert_sql)
            connection.commit()

            
def main():
    index = requests.get(url)
    #is our file there?
    matches = m.search(index.text)
    if matches:
        file = domain + matches.groupdict()['filename']
        pieces = file.split('/')
        #we'll create this file ...
        target = data_dir + pieces.pop()
        #unless we've already grabbed it.
        if not path.exists(target):
            fetch_and_format(file, target)
            insert_data(table, raw_table)
if __name__ == '__main__':
    main()

