#!/usr/bin/env python
#simple utility script to put charges that haven't been catorized in a table we can use to then categorize them.
#hote that this categorization is a largely manual process given that charges are free-form.
#this is ultimately used to update the lookup table charge_catgories

import MySQLdb
from scraper_config import make_config

home_dir, data_dir, database, db_user, db_pw, commands_url = make_config()

sql_truncate = 'truncate charges'
sql_arrests = 'insert into charges select distinct arrests.charge from arrests left join charge_categories on arrests.charge = charge_categories.charge where charge_categories.charge is null'
sql_incidents = 'insert into charges select distinct incidents.charge from incidents left join charge_categories on incidents.charge = charge_categories.charge where charge_categories.charge is null'


connection = MySQLdb.connect(user=db_user,passwd=db_pw,db=database)
cursor = connection.cursor()

def query(sql):
    cursor.execute(sql)
    connection.commit()

def main():
    query(sql_truncate)
    query(sql_arrests)
    query(sql_incidents)

if __name__ == "__main__":
    main()

