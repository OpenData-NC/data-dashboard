import re
import datetime
import hashlib
import json
import time
import requests
from bs4 import BeautifulSoup

from scraper_commands import all_data, check_data
from date_formatters import *
from store_pdf import *
from scrape_logs import *


main_url = ''
json_url = 'http://p2c.nhcgov.com/p2c/jqHandler.ashx?op=s'
s = requests.Session()

# make an array of formatted dates we'll use to grab
#each of the bulletin pages

#should probably rename this and the next function
#this one grabs the record type (arrest, incident, etc.)
# and, if available, the record id
def parse_id_and_type(row):
    record_types = {'LW': 'Incident', 'AR': 'Arrest', 'TA': 'Accident', 'TC': 'Citation', 'OR': 'Citation'}
    record_type = record_types[row['key']]
    if row['id'] == '&nbsp;':
        row['id'] = ''

    record_id = row['id']
    return {'record_id': record_id, 'record_type': record_type}


#this one decides what parsing function to call based on record type.
#piece is the beautifulsoup table row that contains our data
#id_and_type is a dict with those items
#officer is a dict with the reporting officer

def parse_details(row, id_and_type, officer):
    if id_and_type['record_type'] == 'Incident':
        data = parse_incident(row, id_and_type, officer)
    elif id_and_type['record_type'] == 'Arrest':
        data = parse_arrest(row, id_and_type, officer)
    elif id_and_type['record_type'] == 'Citation':
        data = parse_citation(row, id_and_type, officer)
    else:
        data = parse_accident(row, id_and_type, officer)
    #data contains a dict with the items we pulled and formatted
    #we append that to the record_type array in all data
    #build a single all_data to print later
    if data is None:
        return
    return all_data[id_and_type['record_type']].append(check_data(data))


#each of the following four functions parse specific record types

def parse_incident(row, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    data = {}
    name_rsa = row['name'].split(" (")
    data['name'] = name_rsa[0].strip()
    if len(name_rsa) > 1:
        rsa = name_rsa[1].split(')')
        data['rsa'] = rsa[0]
    data = race_sex_age(data)


    m = re.compile('(?P<on_or_between>between|on) (?P<occurred_date>[^\.]+)\. Reported: (?P<reported_date>[^\.]+)\.')
    matches = m.search(row['time'])
    data = dict(data.items() + matches.groupdict().items())
    m = re.compile('VICTIM of (?P<charge>.+) ?\((?P<offense_code>[A-Z ]?)\)?')
    matches = m.search(row['crime'])
    data = dict(data.items() + matches.groupdict().items())
    m = re.compile('at (?P<address>.+),? ?$')
    matches = m.search(row['location'])
    if matches:
        data = dict(data.items() + matches.groupdict().items())
    data = on_between(data)
    data['date_reported'] = format_db_date_part(data['reported_date'])
    data['time_reported'] = format_db_time_part(data['reported_date'])
    data = format_reported_date(data, 'reported_date')
    data['pdf'] = find_pdf(data, id_and_type)
    data['charge'] = data['charge'].strip()
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_arrest(row, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    data = {}
    name_rsa = row['name'].split(" (")
    data['name'] = name_rsa[0].strip()
    if len(name_rsa) > 1:
        rsa = name_rsa[1].split(')')
        data['rsa'] = rsa[0]
    data = race_sex_age(data)


    m = re.compile('on (?P<occurred_date>[^\.]+)\.')
    matches = m.search(row['time'])
    data = dict(data.items() + matches.groupdict().items())
    data['charge'] = row['charge'].split(',')[0].strip()
    m = re.compile('\(*(?P<offense_code>[A-Z ]*)\)*,*$')
    matches = m.search(row['crime'])
    data = dict(data.items() + matches.groupdict().items())
    m = re.compile('at (?P<address>.+),? ?$')
    matches = m.search(row['location'])
    if matches:
        data = dict(data.items() + matches.groupdict().items())
    if id_and_type['record_id'] == '':
        other_data['id_generate'] = "1"
        if 'address' not in data:
            data['address'] = ''
        id_and_type['record_id'] = hashlib.sha224(data['name'] + data['occurred_date'] + data['address']
                                                  + data['charge']).hexdigest()
    else:
        data['date_reported'] = format_db_date(data['occurred_date'].split(' ')[0])
        data['pdf'] = find_pdf(data, id_and_type)

    data = format_date_time(data, 'occurred_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_citation(row, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    text = row['description']
    m = re.compile(
        '(?P<name>.+) \((?P<rsa>.*)\) Cited on Charge of (?P<charge>.+), at (?P<address>.+), +'
        'on +(?P<occurred_date>.+)\.')
    matches = m.search(text)
    if not matches:
        m = re.compile('(?P<name>.+) \((?P<rsa>.*)\) Cited on Charge of (?P<charge>.+)')
        matches = m.search(text)
    data = matches.groupdict()
    data = race_sex_age(data)
    data = format_date_time(data, 'occurred_date')
    return dict(data.items() + officer.items() + id_and_type.items() + other_data.items())


def parse_accident(piece, id_and_type, officer):
    other_data = {'scrape_type': 'bulletin', 'id_generate': '0'}
    m = re.compile('On (?P<occurred_date>.+) at (.*), an accident occured on'
                   ' +(?P<address>[^\.]+)\..+Accident involving: (?P<names>.+)')
    matches = m.search(piece.text)
    data = matches.groupdict()
    # names might be more than one
    data = people_in_accident(data)
    data = format_date_time(data, 'occurred_date')
    data['date_reported'] = format_db_date(data['occurred_date'].split(' ')[0])
    data['pdf'] = find_pdf(data,id_and_type)
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


def find_pdf(data, id_and_type):
    #    print id_and_type
    global main_url
    if main_url == '':
        return ''
    page = s.get(main_url)
    soup = BeautifulSoup(page.text)
    payload = extract_form_fields(soup)
    types = {'Arrest': 'AR', 'Accident': 'TA', 'Incident': 'LW', 'Citation': 'TC'}
    this_type = types[id_and_type['record_type']]
    #try to figure out what version it is
    if 'MasterPage$mainContent$txtDateFrom2' in payload:
        payload['MasterPage$mainContent$txtDateFrom2'] = payload[
            'MasterPage$mainContent$txtDateTo2'] = format_search_date(data['date_reported'])
        payload['MasterPage$mainContent$txtCase2'] = id_and_type['record_id']
        payload['MasterPage$mainContent$rblSearchDateToUse2'] = 'Date Reported'
        payload['__EVENTTARGET'] = 'MasterPage$mainContent$cmdSubmit2'
    if 'ctl00$mainContent$txtDateFrom2' in payload:
        payload['ctl00$mainContent$txtDateFrom2'] = payload[
            'ctl00$mainContent$txtDateTo2'] = format_search_date(data['date_reported'])
        if 'ct100$mainContent$btnReset' in payload:
            del payload['ct199$mainContent$btnReset']
        if 'MasterPage$DDLSiteMap1$ddlQuickLinks' in payload and payload['MasterPage$DDLSiteMap1$ddlQuickLinks'] == '':
            del payload['MasterPage$DDLSiteMap1$ddlQuickLinks']
        payload['ctl00$mainContent$txtCase2'] = id_and_type['record_id']
        payload['ctl00$mainContent$rblSearchDateToUse2'] = 'Date Reported'
        payload['__EVENTTARGET'] = 'ctl00$mainContent$cmdSubmit2'
    if 'MasterPage$mainContent$txtDateFrom$txtDatePicker' in payload:
        payload['MasterPage$mainContent$txtDateFrom$txtDatePicker'] = payload[
            'MasterPage$mainContent$txtDateTo$txtDatePicker'] = format_search_date(
            data['date_reported'])
        if 'MasterPage$mainContent$btnReset' in payload:
            del payload['MasterPage$mainContent$btnReset']
        if 'MasterPage$DDLSiteMap1$ddlQuickLinks' in payload and payload['MasterPage$DDLSiteMap1$ddlQuickLinks'] == '':
            del payload['MasterPage$DDLSiteMap1$ddlQuickLinks']
        payload['MasterPage$mainContent$txtCase'] = id_and_type['record_id']
        payload['MasterPage$mainContent$rblSearchDateToUse'] = 'Date Reported'
        payload['__EVENTTARGET'] = 'Search'
    if 'ctl00$mainContent$txtDateFrom$txtDatePicker' in payload:
        payload['ctl00$mainContent$txtDateFrom$txtDatePicker'] = payload[
            'ctl00$mainContent$txtDateTo$txtDatePicker'] = format_search_date(data['date_reported'])
        if 'ctl00$mainContent$btnReset' in payload:
            del payload['ctl00$mainContent$btnReset']
        payload['ctl00$mainContent$txtCase'] = id_and_type['record_id']
        payload['ctl00$mainContent$rblSearchDateToUse'] = 'Date Reported'
        payload['ctl00$mainContent$cmdSubmit'] = 'Search'
        payload['__EVENTTARGET'] = ''
        payload['__EVENTARGUMENT'] = ''
        payload['__LASTFOCUS'] = ''
    #check to see if our type is available. if it is, only
    #only search for that type. incidents and arrests on the same event
    #sometimes have the same case number
    payload['__LASTFOCUS'] = ''
    found_type = False
    check_payload = dict(payload.items())
    for key, value in check_payload.iteritems():
        if value == 'on':
            if key.find(this_type) != -1:
                found_type = True
            else:
                del payload[key]
            #the type of record we're searching for isn't available
            #via aearch
    if not found_type:
        return ''
    referer = {'Referer': main_url}
    page = s.post(main_url, data=payload, headers=referer)
    soup = BeautifulSoup(page.text)
    records = soup.find_all('table', {'class':'DataGridText'})
    if records is not None and len(records) > 0:
        records = records[0].find_all('tr', {'class':'EventSearchGridRow'})
    else:
        return ''
    payload = extract_form_fields(soup)
    # v = soup.find('input', {'id': "__VIEWSTATE"})['value']
    # e = soup.find('input', {'id': "__EVENTVALIDATION"})['value']
    # v_e = {'__VIEWSTATE': v, '__EVENTVALIDATION': e}
    #we should only have one. if not, something's wrong
    if not records or len(records) > 1:
        return ''
    for record in records:
        record_fields = record.find_all('td', attrs={'class': None})
        field_wanted = len(record_fields) - 1
        if record_fields[field_wanted].find('img'):
            has_gif = record_fields[field_wanted].find('img')['src']
        else:
            return ''
        if has_gif == 'images/noimage.gif':
            #there's no pdf
            return ''
        report = record_fields[field_wanted].find('a')['href']
        report.replace('%#39;',"'")
        if report is not None:
            m = re.compile(r"'(?P<first>[^']*)','(?P<second>[^']*)'")
            matches = m.search(report)
            data = matches.groupdict()
            target = data['first']
            argument = data['second']
            return dl_pdf(target, argument, id_and_type, payload, main_url)


def dl_pdf(target, argument, id_and_type, payload, url):
    if target == '' or target is None:
        return ''
    pdf_file = store_pdf.create_file_name(id_and_type['record_id'],id_and_type['record_type'],id_and_type['agency'])
    if store_pdf.file_exists(pdf_file):
        return pdf_file
    payload['__EVENTTARGET'] = target
    if 'ctl00$mainContent$btnReset' in payload:
        del payload['ctl00$mainContent$btnReset']
    if 'ctl00$mainContent$cmdSubmit' in payload:
        del payload['ctl00$mainContent$cmdSubmit']
    if argument != '':
        payload['__EVENTARGUMENT'] = argument
    referer = {'Referer': url}
    pdf_response = s.post(url, data=payload, headers=referer, allow_redirects=True, stream=True)
    pdf_file = store_pdf.store_file(pdf_response,pdf_file)
    return pdf_file


def pass_disclaimer(url):
    #    print "Passing disclaimer"
    page = s.get(url)
    if page.url != url:
        disclaimer_url = page.url
        soup = BeautifulSoup(page.text)
        payload = extract_form_fields(soup)
        referer = {'Referer': disclaimer_url}
        page = s.post(disclaimer_url, data=payload, headers=referer)


#        types_available(page)



def types_available(page):
    global search_items
    soup = BeautifulSoup(page.text)
    checkboxes = soup.find_all('input', {'type': 'checkbox'})
    for checkbox in checkboxes:
        search_items[checkbox['name']] = 'on'


def extract_form_fields(soup):
    fields = {}
    for input in soup.findAll('input'):
        # ignore submit/image with no name attribute
        if input['type'] in ('submit', 'image') and not input.has_attr('name'):
            continue

        # single element nome/value fields
        if input['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            value = ''
            if input.has_attr('value'):
                value = input['value']
            fields[input['name']] = value
            continue

        # checkboxes and radios
        if input['type'] in ('checkbox', 'radio'):
            value = ''
            if input.has_attr('checked'):
                if input.has_attr('value'):
                    value = input['value']
                else:
                    value = 'on'
            if fields.has_key(input['name']) and value:
                fields[input['name']] = value

            if not fields.has_key(input['name']):
                fields[input['name']] = value

            continue

        assert False, 'input type %s not supported' % input['type']

    # textareas
    for textarea in soup.findAll('textarea'):
        fields[textarea['name']] = textarea.string or ''

    # select fields
    for select in soup.findAll('select'):
        value = ''
        options = select.findAll('option')
        is_multiple = select.has_attr('multiple')
        selected_options = [
            option for option in options
            if option.has_attr('selected')
        ]

        # If no select options, go with the first one
        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            assert (len(selected_options) < 2)
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]

        fields[select['name']] = value

    return fields


def find_v_e(page):
    soup = BeautifulSoup(page)
    v = soup.find('input', {'id': "__VIEWSTATE"})['value']
    e = soup.find('input', {'id': "__EVENTVALIDATION"})['value']
    return {'__VIEWSTATE': v, '__EVENTVALIDATION': e}


def try_bulletin(url):
    global main_url
    main_url = url
    if url.find('Summary') != -1:
        bulletin_url = re.sub('Summary', 'dailybulletin', url)
    else:
        bulletin_url = url
        main_url = ''
    page = requests.get(bulletin_url)
    if page.url != bulletin_url:
        return False
    pass_disclaimer(url)
    return bulletin_url


def start_scrape(agency, county, url, howfar):
    """

    :param url: The url to the daily bulletin
    :param howfar: How many days back to scrape
    """
    json_params = {'t': 'db', '_search': 'false', 'rows': 10000, 'nd': '', 'page': '1', 'sidx': 'case', 'sort': 'asc'}
    keys_wanted = ['key','id','name','crime','location','time']
    dates = make_dates(agency, howfar)
    for date in dates:
        page = s.get(url)
        soup = BeautifulSoup(page.text.encode('utf-8'))
        payload = extract_form_fields(soup)
        payload['MasterPage$mainContent$txtDate2'] = date
        payload['__EVENTTARGET'] = 'MasterPage$mainContent$lbUpdate'
        referer = {'Referer': url}
        page = s.post(url, data=payload, headers=referer)
        json_params['nd'] = int(time.time() *1000)
        page = s.post(json_url,data=json_params,headers=referer)
        rows = json.loads(page.text)['rows']
        for row in rows:

            this_row = [row[key] for key in keys_wanted]
            id_type_agency = dict(
                parse_id_and_type(row).items() + {'agency': agency, 'county': county}.items())
            reporting_officer = {'reporting_officer': row['officer']}
            parse_details(row, id_type_agency, reporting_officer)
        # for incident_type, incidents in all_data.iteritems():
        #     for incident in incidents:
        #         print incident
    return all_data
