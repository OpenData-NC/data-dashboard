#!/usr/bin/env python

from scrape_bulletin_nh import try_bulletin, start_scrape
from scraper_config import make_config
from scraper_commands import print_files, all_data
from db_load import db_load


def main():
    #fetch data from our google spreadsheet that tells us what to scrape
    home_dir, data_dir, database, db_user, db_pw, commands_url = make_config('_nh')
    site = {'URL': 'http://p2c.nhcgov.com/p2c/Summary.aspx','Agency':"New Hanover County Sheriff's Office",'County': 'New Hanover','How far back':'7'}
    #variables we'll use in our scraping and data format
    county = site['County']
    url = site['URL']
    agency = site['Agency']
    #this is how many days back we want to scrape
    #e.g. 1 would scrape a total of 2 days:
    # today plus 1 day back (yesterday)
    howfar = int(site['How far back'])
    #try for daily bulletin
    bulletin_url = try_bulletin(url)
    start_scrape(agency, county, bulletin_url, howfar)
    #output data as tab-delimited text files named for the
    #record type (arrest.txt, incident.txt, citation.txt, accident.txt)
    print_files(scraper_commands.all_data,data_dir)
    for data_type in all_data:
        data_file = data_dir + '/' + data_type + '.txt'
        table = data_type.lower() + 's'
        load(database,data_file, table, user)
if __name__ == "__main__":
    main()
