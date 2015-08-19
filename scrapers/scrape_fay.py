#!/usr/bin/env python
#pull data from fayetteville, nc, pd's p2c site
#this is custom because that site is so different from others
import scrape_bulletin
import scrape_search_fay
from scraper_commands import check_data, print_files, fetch_commands, all_data
from db_load import db_load

from scraper_config import make_config

home_dir, data_dir, database, db_user, db_pw, commands_url = make_config()

data_dir = home_dir + 'data_fay'
database = 'crime'
user = {'user': 'crimeloader','pw':'redaolemirc'}

def main():
    #fetch data from our google spreadsheet that tells us what to scrape
    sites_to_scrape = [{'URL': 'http://p2c.bethebadge.com/p2c/Summary.aspx','Agency':'Fayetteville Police Department','County': 'Cumberland','How far back':'7'}]
    for site in sites_to_scrape:
        #variables we'll use in our scraping and data format
        county = site['County']
        url = site['URL']
        agency = site['Agency']
        #this is how many days back we want to scrape
        #e.g. 1 would scrape a total of 2 days:
        # today plus 1 day back (yesterday)
        howfar = int(site['How far back'])
        #try for daily bulletin
        #if not, then go for search
        bulletin_url = scrape_bulletin.try_bulletin(url)
        if bulletin_url:
            data = scrape_bulletin.start_scrape(agency, bulletin_url, howfar)
        else:
            data = scrape_search_fay.start_scrape(agency, url, howfar, county)
#        for record_type in data:
#            scraper_commands.all_data[record_type] = scraper_commands.all_data[record_type] + data[record_type]
    #output data as tab-delimited text files named for the
    #record type (arrest.txt, incident.txt, citation.txt, accident.txt)
    scraper_commands.print_files(scraper_commands.all_data,data_dir)
    for data_type in scraper_commands.all_data:
        data_file = data_dir + '/' + data_type + '.txt'
        table = data_type.lower() + 's'
        db_load(database,data_file, table, db_user, db_pw)
if __name__ == "__main__":
    main()
