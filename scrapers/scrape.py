#!/usr/bin/env python
import scrape_bulletin
#import scrape_search
import sys
from scraper_config import make_config
from scraper_commands import check_data, print_files, fetch_commands, all_data
from db_load import db_load

def main():
    home_dir, data_dir, database, db_user, db_pw, commands_url = make_config()
    sites_to_scrape = fetch_commands(commands_url)
    #pick out site we want as index from list of sites
    #passed as an argument to this script
    site = sites_to_scrape[int(sys.argv[1])]
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
        if bulletin_url == 'unreachable':
            print "\t".join([url,bulletin_url])
        else:
            data = scrape_bulletin.start_scrape(agency, county, bulletin_url, howfar)
    else:
        #we'll need to import the functionality to scrape a search site
        import scrape_search
        data = scrape_search.start_scrape(agency, url, howfar, county)
        if not data:
            print "\t".join([url,"failed"])
    #output data as tab-delimited text files named for the
    #record type (arrest.txt, incident.txt, citation.txt, accident.txt)
    print_files(all_data,data_dir, site['Site'])
    exit()
    for data_type in all_data:
        data_file = data_dir + '/' + site['Site'] + data_type + '.txt'
        table = data_type.lower() + 's'
        db_load(database,data_file, table, db_user, db_pw)
        
        
if __name__ == "__main__":
    main()
