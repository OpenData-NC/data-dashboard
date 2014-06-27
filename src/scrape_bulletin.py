import re
import datetime
import hashlib

import scraper_commands
import date_formatters
import requests
from bs4 import BeautifulSoup

#make an array of formatted dates we'll use to grab
#each of the bulletin pages

#should probably rename this and the next function
#this one grabs the record type (arrest, incident, etc.)
# and, if available, the record id
def parse_id_and_type(piece):
    record_types = {'LW': 'Incident', 'AR': 'Arrest', 'TA': 'Accident', 'TC': 'Citation', 'OR': 'Citation'}
    items = piece.text.split(" ")
    record_type = record_types[items[0]]
    if record_type == 'Accident':
        record_id = items.pop()
    else:
        record_id = piece.find('br').previous_sibling.split(" ").pop()
    return {'record_id': record_id, 'record_type': record_type}

#this one decides what parsing function to call based on record type.
#piece is the beautifulsoup table row that contains our data
#id_and_type is a dict with those items
#officer is a dict with the reporting officer

def parse_details(piece, id_and_type, officer):
    if id_and_type['record_type'] == 'Incident':
        data = parse_incident(piece, id_and_type, officer)
    elif id_and_type['record_type'] == 'Arrest':
        data = parse_arrest(piece, id_and_type, officer)
    elif id_and_type['record_type'] == 'Citation':
        data = parse_citation(piece, id_and_type, officer)
    else:
        data = parse_accident(piece, id_and_type, officer)
    #data contains a dict with the items we pulled and formatted
    #we append that to the record_type array in all data
    #build a single all_data to print later
    if data is None:
        return
    return scraper_commands.all_data[id_and_type['record_type']].append(scraper_commands.check_data(data))

#each of the following four functions parse specific record types

def parse_incident(piece, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    m = re.compile(
        '(?P<name>.*) *\((?P<rsa>.*)\) ?VICTIM of (?P<charge>[^.]+) \((?P<offense_code>[A-Z ])\), '
        'at (?P<address>.+), +(?P<on_or_between>between|on) (?P<occurred_date>[^\.]+)\. Reported: '
        '(?P<reported_date>[^\.]+)\.')
    matches = m.search(piece.text)
    if not matches:
        m = re.compile(
            '(?P<name>.*) VICTIM of (?P<charge>[^.+]+) \((?P<offense_code>[A-Z ])\), at (?P<address>.+),'
            ' +(?P<on_or_between>between|on) (?P<occurred_date>[^\.]+)\. Reported: (?P<reported_date>[^\.]+)\.')
        matches = m.search(piece.text)
    data = matches.groupdict()
    data = race_sex_age(data)
    data = date_formatters.on_between(data)
    data['date_reported'] = date_formatters.format_db_date_part(data['reported_date'])
    data['time_reported'] = date_formatters.format_db_time_part(data['reported_date'])
    data = date_formatters.format_reported_date(data, 'reported_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_arrest(piece, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    m = re.compile('(?P<name>[^()]+) Arrest on chrg of (?P<charge>[^(]+) \(*?P<offense_code>[A-Za-z]?\)?'
                   ' ?\(?(?P<other_code>.?)\)?, at (?P<address>.+), +on +(?P<occurred_date>[^\.]+)\.')
    matches = m.search(piece.text)
    if matches:
        matches = matches
    else:
        m = re.compile('(?P<name>.+) \((?P<rsa>.*)\) Arrest on chrg of (?P<charge>[^(]+) '
                       '\(?(?P<offense_code>[A-Za-z]?)\)? ?\(?(?P<other_offense_code>.?)\)?, '
                       'at (?P<address>.+), +on +(?P<occurred_date>.+)\.')
        matches = m.search(piece.text)
        if not matches:
            m = re.compile('(?P<name>.+) \((?P<rsa>.*)\) Arrest on chrg of (?P<charge>[^(]+) '
                           '\(?(?P<offense_code>[A-Za-z]?)\)? ?\(?(?P<other_offense_code>.?)\)?, '
                           '.+, +on +(?P<occurred_date>[^\.]+)\.')
            matches = m.search(piece.text)
        # skip this one if there's not enough info
        if not matches:
            return
    data = matches.groupdict()
    data = race_sex_age(data)
    if id_and_type['record_id'] == '':
        other_data['id_generated'] = "1"
        if 'address' not in data:
            data['address'] = ''
#        id_and_type['record_id'] = hashlib.sha224( + matches[0][2] + matches[0][3] + matches[0][4] + matches[0][5]) \
        id_and_type['record_id'] = hashlib.sha224(data['name'] + data['occurred_date'] + data['address']
             + data['charge']).hexdigest()
    data = date_formatters.format_date_time(data, 'occurred_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_citation(piece, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    m = re.compile(
        '(?P<name>.+) \((?P<rsa>.*)\) Cited on Charge of (?P<charge>.+), at (?P<address>.+), +'
        'on +(?P<occurred_date>.+)\.')
    matches = m.search(piece.text)
    if not matches:
        m = re.compile('(?P<name>.+) \((?P<rsa>.*)\) Cited on Charge of (?P<charge>.+)')
        matches = m.search(piece.text)
    data = matches.groupdict()
    data = race_sex_age(data)
    data = date_formatters.format_date_time(data, 'occurred_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_accident(piece, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    m = re.compile('On (?P<occurred_date>.+) at (.*), an accident occured on'
                   ' +(?P<address>[^\.]+)\..+Accident involving: (?P<names>.+)')
    matches = m.search(piece.text)
    data = matches.groupdict()
    # names might be more than one
    data = people_in_accident(data)
    data = date_formatters.format_date_time(data, 'occurred_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def race_sex_age(data):
    rsa = {'race': '', 'sex': '', 'age': ''}
    if 'rsa' in data and data['rsa'] != '':
        m = re.compile('(?P<race>[A-Z])[ /]*(?P<sex>[A-Z])[,/ ]*(?P<age>\d+)');
        matches = m.search(data['rsa'])
        if matches:
            rsa = matches.groupdict()
#        pieces = data['rsa'].split('/')
#        pieces[0] = pieces[0].strip()
#        rsa = {'race': pieces[0], 'sex': pieces[1], 'age': pieces[2]}
    return dict(data.items() + rsa.items())


def people_in_accident(data):
    names = {'name1': '', 'name2': ''}
    people = data['names'].split(', ')
    for i in range(len(people)):
        if i < 2:
            key = 'name' + str(i + 1)
            names[key] = people[i]
    return dict(data.items() + names.items())

def try_bulletin(url):
    bulletin_url = re.sub('Summary', 'dailybulletin', url)
    page = requests.get(bulletin_url)
    if page.url != bulletin_url:
        return False
    return bulletin_url


def start_scrape(agency, url, howfar):
    """

    :param url: The url to the daily bulletin
    :param howfar: How many days back to scrape
    """
    print_url = re.sub('dailybulletin', 'DailyBulletinPrint', url)
    s = requests.Session()
    s.get(url)
    dates = date_formatters.make_dates(howfar)
    for date in dates:
        payload = {'Date': date, 'Type': 'AL'}
        referer = {'Referer': url}
        page = s.get(print_url, params=payload, headers=referer)
	soup = BeautifulSoup(page.text.encode('utf-8'))
        count = 0
        for row in soup.find_all('table', id="dgBulletin")[0].find_all('tr'):
            if count == 0:
                count += 1
            else:
                # if not row.has_attr('bgcolor'):
                pieces = row.findAll('td')
                id_type_agency = dict(parse_id_and_type(pieces[0]).items() + {'agency': agency}.items())
                reporting_officer = {'reporting_officer': pieces[2].text}
                parse_details(pieces[1], id_type_agency, reporting_officer)
    # for incident_type, incidents in scraper_commands.all_data.iteritems():
    #     for incident in incidents:
    #         print incident
    return scraper_commands.all_data
