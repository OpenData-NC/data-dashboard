import scrape_bulletin
import scrape_search
import scraper_commands

commands_url = \
    'https://docs.google.com/spreadsheets/d/1353q8QCgtscYRBU0INeOKIhPAiXt2IXpdTjD3ufl8Ko/export?gid=0&format=csv'


def main():
    #fetch data from our google spreadsheet that tells us what to scrape
    sites_to_scrape = scraper_commands.fetch_commands(commands_url)
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
        print url
        if bulletin_url:
            data = scrape_bulletin.start_scrape(agency, bulletin_url, howfar)
        else:
            data = scrape_search.start_scrape(agency, url, howfar, county)
        for record_type in data:
            scraper_commands.all_data[record_type] = scraper_commands.all_data[record_type] + data[record_type]
    #output data as tab-delimited text files named for the
    #record type (arrest.txt, incident.txt, citation.txt, accident.txt)
    scraper_commands.print_files(scraper_commands.all_data)

if __name__ == "__main__":
    main()
