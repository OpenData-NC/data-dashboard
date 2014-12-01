#!/usr/bin/env python
import scrape_bulletin
import scrape_search
import scraper_commands
import db_load
import sys
home_dir = '/home/vaughn.hagerty/crime-scrapers/'
data_dir = home_dir + 'data'
database = 'crime'
user = {'user': 'crimeloader','pw':'redaolemirc'}
commands_url = \
    'https://docs.google.com/spreadsheets/d/1353q8QCgtscYRBU0INeOKIhPAiXt2IXpdTjD3ufl8Ko/export?gid=0&format=csv'


def main():
    sites_to_scrape = scraper_commands.fetch_commands(commands_url)
    #pick out site we want as index from list of sites
    site_wanted = sites_to_scrape( int(sys.argv[1]) )    
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
        data = scrape_search.start_scrape(agency, url, howfar, county)
        if not data:
            print "\t".join([url,"failed"])
    #output data as tab-delimited text files named for the
    #record type (arrest.txt, incident.txt, citation.txt, accident.txt)
    scraper_commands.print_files(scraper_commands.all_data,data_dir, site['site'])
    for data_type in scraper_commands.all_data:
        data_file = data_dir + '/' + site['site'] + data_type + '.txt'
        table = data_type.lower() + 's'
        db_load.load(database,data_file, table, user)
        
        
if __name__ == "__main__":
    main()
