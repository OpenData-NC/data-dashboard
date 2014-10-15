import MySQLdb
import requests
import datetime
import re
from os import path
from subprocess import call

data_dir = '/home/vaughn.hagerty/health_inspections/data'
accumulator = ''
url = 'http://ehs.ncpublichealth.com/browsablemedia/'
pattern = datetime.datetime.now().strftime('%m\d\d%y') + '\.txt'
m = re.compile(pattern)
user = {'user': 'vhagerty', 'pw': 'snook1eB0y'}
table = 'rr'
raw_table = 'rr_raw'
database = 'general'
connection = MySQLdb.connect(user=user['user'],passwd=user['pw'],db=database)
cursor = connection.cursor()


def format_and_load():
    sql = "SELECT FACILITY_ID_NUMBER, FAC_TYPE, COUNTY_ID, FAC_NAME \
            , ADDR_LINE1, ADDR_CITY, ADDR_ZIP5, ACTIVITY_DATE, STATUS_CODE, ACTIVITY_SCORE \
            , ACTIVITY_FINAL_SCORE, ACTIVITY_GENERAL_COMMENT, ITEM_COMMENTS from %s" % (raw_table)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        row = list(row)
        row[7] = datetime.datetime.strptime(row[7], '%d-%b-%y').strftime('%Y/%m/%d')
        row[3] = MySQLdb.escape_string(row[3])
        row[11] = MySQLdb.escape_string(row[3])
        row[12] = MySQLdb.escape_string(row[3])
        check_sql = 'select * from ' + table + ' where facility_id = "' + row[0] + '" and activity_date = "' + row[7] + '"'
        cursor.execute(check_sql)
        found = cursor.fetchall()
        if not len(found):
            values = '("' + '","'.join(row) + '")'
            insert_sql = 'insert into ' + table + ' values ' + values
            cursor.execute(insert_sql)
            connection.commit()

def fetch_raw_data(file, target):
    accumulator = ''
    fetch_command = 'wget -q -P ' + data_dir + ' ' + file
    call(fetch_command, shell=True)
    load(database, target, raw_table, user)

    
def load(database,data_file, table, user):
    load_command = 'mysql --local-infile --user=' + user['user'] + ' --password=' + user['pw'] + ' ' + database + ' -e '\
    + '"truncate ' + table + ';load data local infile \'' + data_file + '\' '\
    + 'into table ' + table.lower() + " fields optionally enclosed by '\\\"'" + " lines terminated by '\\" + "r\\" \
    + "n'" + ' ignore 1 lines";'
    call(load_command,shell=True)


def main():
    index = requests.get(url)
    matches = m.search(index.text)
    if matches:
        file = url + matches.group()
        target = data_dir + '/' + matches.group()
        if not path.exists(target):
            fetch_raw_data(file, target)
			format_and_load()


if __name__ == '__main__':
    main()
