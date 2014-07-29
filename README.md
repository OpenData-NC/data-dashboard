OSSI crime scrapers
===================

Scripts to scrape data from OSSI P2C sites.

What is this?
-------------

A set of Python scripts to scrape data from law enforcement agency web sites that use SunGuard's OSSI P2C system. This is a work in progress and is part of INSERT NAME OF PROJECT HERE.

IMPORTANT: These scripts aren't finished. There is some inline documentation, but they need further testing and a bunch of cleanup. Also, some functionality is not yet included, as noted below.

The script scrape.py pulls from a [Google spreadsheet](https://docs.google.com/spreadsheets/d/1353q8QCgtscYRBU0INeOKIhPAiXt2IXpdTjD3ufl8Ko) that has fields describing each agency site to scrape. Those fields include: Agency name, city, county, the main URL of the P2C site and how many days back to scrape.

If the P2C site has a [daily bulletin](http://p2c.wakeso.net/dailybulletin.aspx), we try to scrape that. If not, we use the site's ["Event Search" interface](http://p2c.wakeso.net/Summary.aspx).

The data is being compiled into tab-delimited files based on record type (accident, arrest, citation, incident) and loaded into a database. Ultimately we will:

* load that data into database tables
* geocode and standardize addresses
* where available, pull PDFs of the actual reports
* create an admin interface to search the data

Assumptions
-----------

Python (of course)
Google spreadsheets
The following non-standard Python modules:
* Requests
* BeautifulSoup
* python-slugify
What's in here
--------------

* src/scrape.py: One script to rule them all. Imports the others, grabs the Google spreadsheet data, scrapes each site and prints out the data files.
* src/scraper_commands.py: Functions to pull and format the Google spreadsheet, to make sure we have spots for all the data fields and to print out the tab-delimited data files.
* src/date_formatters.py: Functions to format dates in the vaarious ways we need them (just date, just time, database format, for submitting in forms)
* src/db_load.py: First iteration of function to load our data using local infile and replace.
* src/store_pdf.py: Functions to create file names and directory structure and to store PDFs of reports downloaded from sites (only on search scrapes for now)
* src/scrape_bulletin.py: Functions specific to pulling and formatting data from sites that have Daily Bulletins available
* src/scrape_search.py: Functions specific to pulling and formatting data from sites that don't have Daily Bulletins. Instead, we use the Event Search.
* src/scrape_fay.py: Main script for custom Fayetteville PD scraper. Imports the others.
* src/scrape_search_fay.py: Functions specific to pulling and formatting data for Fayetteville.
* src/scrape_nh.py: Main script for custom New Hanover County SO scraper. Imports the others.
* src/scrape_bulletin_nh.py: Functions specific to pulling and formatting data for New Hanover.

* sql/crime_scrapers.sql: SQL to create our tables
* data/[various].txt: Example output of the tab-delimited files created by the scripts
* pdf/...: Examples of downloaded report PDFs
