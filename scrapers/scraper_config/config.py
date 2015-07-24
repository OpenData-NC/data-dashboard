#!/usr/bin/env python

#change these to match your values
def make_config(dir_append=''):
    #home directory of everything
    home_dir = '/home/vaughn.hagerty/crime-scrapers/'
    #we create tab-delimited files to import into MySQL via the load data local infile command
    #they live in this directory
    data_dir = home_dir + 'data' + dir_append
    #MySQL configs
    database = 'crime'
    db_user = 'crimeloader'
    db_pw = 'redaolemirc'
    #the source site urls, number of days to scrape and other info is stored in a google spreadsheet
    #we slurp it as csv
    commands_url = \
        'https://docs.google.com/spreadsheets/d/1353q8QCgtscYRBU0INeOKIhPAiXt2IXpdTjD3ufl8Ko/export?gid=0&format=csv'
    return (home_dir, data_dir, database, db_user, db_pw, commands_url)
