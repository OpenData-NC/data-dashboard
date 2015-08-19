#!/usr/bin/env python

#change these to match your values
def make_config(dir_append=''):
    #home directory of everything
    home_dir = '[where your scraper scripts live on the server]'
    #we create tab-delimited files to import into MySQL via the load data local infile command
    #they live in this directory
    data_dir = home_dir + 'data' + dir_append
    #MySQL configs
    database = '[database name]'
    db_user = '[db user with insert, update, select, delete permissions on database]'
    db_pw = '[that db user pw]'
    #the source site urls, number of days to scrape and other info is stored in a google spreadsheet
    #we slurp it as csv
    commands_url = \
        '[the url to the *CSV* output of your google spreadsheet]'
    return (home_dir, data_dir, database, db_user, db_pw, commands_url)
