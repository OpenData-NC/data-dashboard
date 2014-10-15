#!/usr/bin/env python

import MySQLdb


sql_truncate = 'truncate charges'
sql_arrests = 'insert into charges select distinct arrests.charge from arrests left join charge_categories on arrests.charge = charge_categories.charge where charge_categories.charge is null'
sql_incidents = 'insert into charges select distinct incidents.charge from incidents left join charge_categories on incidents.charge = charge_categories.charge where charge_categories.charge is null'

user = 'crimeloader'
pw = 'redaolemirc'
db = 'crime'

connection = MySQLdb.connect(user=user,passwd=pw,db=db)
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

