import requests
from bs4 import BeautifulSoup
import datetime
import re
import shutil
import hashlib

import scraper_commands
#import bing_geocode


disclaimer_items = {'_popupBlockerExists': 'true', '__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '',
                    'ctl00$MasterPage$DDLSiteMap1$ddlQuickLinks': '~/main.aspx',
                    'ctl00$MasterPage$mainContent$CenterColumnContent$btnContinue': 'I Agree'}
search_items = {'__EVENTTARGET': 'MasterPage$mainContent$cmdSubmit2', '__EVENTARGUMENT': '', '__LASTFOCUS': '',
                'MasterPage$DDLSiteMap1$ddlQuickLinks': '~/main.aspx', 'MasterPage$mainContent$txtCase2': '',
                'MasterPage$mainContent$rblSearchDateToUse2': 'Date Occurred',
                'MasterPage$mainContent$ddlDates2': 'Specify Date', 'MasterPage$mainContent$txtLName2': '',
                'MasterPage$mainContent$txtFName2': '', 'MasterPage$mainContent$txtMName2': '',
                'MasterPage$mainContent$txtStreetNo2': '', 'MasterPage$mainContent$txtStreetName2': '',
                'MasterPage$mainContent$ddlNeighbor2': '', 'MasterPage$mainContent$ddlRange2': '',
                'MasterPage$mainContent$addresslat': '', 'MasterPage$mainContent$addresslng': ''}
community_item = {'MasterPage$mainContent$CGeoCityDDL12': ''}  # testing

s = requests.Session()


def types_available(page):
    global search_items
    soup = BeautifulSoup(page.text)
    checkboxes = soup.find_all('input', {'type': 'checkbox'})
    for checkbox in checkboxes:
        search_items[checkbox['name']] = 'on'


def find_v_e(page):
    soup = BeautifulSoup(page)
    v = soup.find('input', {'id': "__VIEWSTATE"})['value']
    e = soup.find('input', {'id': "__EVENTVALIDATION"})['value']
    return {'__VIEWSTATE': v, '__EVENTVALIDATION': e}


def find_range(farback):
    date_wanted = (datetime.datetime.today() - datetime.timedelta(days=farback)).strftime('%m/%d/%Y')
    return {'MasterPage$mainContent$txtDateFrom2': date_wanted, 'MasterPage$mainContent$txtDateTo2': date_wanted}


def make_date_ranges(howfar):
    date_ranges = []
    while howfar >= 0:
        date_ranges.append(find_range(howfar))
        howfar -= 1
    return date_ranges


def format_db_date(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M').strftime('%Y/%m/%d %H:%M')


# remove the stray semicolon beautiful soup adds
def remove_semicolon(text):
    return re.sub(r';$', '', text)


#extract communities
def find_communities(page, county='None'):
    communities_available = {}
    soup = BeautifulSoup(page)
    options = soup.find_all("select", class_="geofields2")[0].find_all("option")
    for option in options:
        if option.string is None:
            community = county
        else:
            community = option.string
        communities_available[community] = option['value']
    return communities_available


#how many pages of records?
def number_of_pages(soup):
    return num(soup.find_all('span', id='mainContent_lblPageCount')[0].find('b').next_sibling.split(' ').pop())


#find records in pages
def find_records(soup, community, agency):
    records = soup.find_all('tr', class_='EventSearchGridRow')
    v = soup.find('input', {'id': "__VIEWSTATE"})['value']
    e = soup.find('input', {'id': "__EVENTVALIDATION"})['value']
    v_e = {'__VIEWSTATE': v, '__EVENTVALIDATION': e}

    for record in records:
#        new_record = [community, '', '', '', '', '', '', '', '', '', '', '', '', '']
        other_data = {'scrape_type': 'search', 'id_generate': '0'}
        data = {}
        id_and_type = {}
        record_fields = record.find_all('td')
        id_and_type['record_type'] = record_fields[2].string.strip()  # record type
        data['occurred_date'] = format_db_date(record_fields[1].string.strip())  # date
        data['address'] = re.sub(r' +', ' ', record_fields[4].string.strip())  #address
        if id_and_type['record_type'] != 'Accident':
            data['charge'] = remove_semicolon(
                record_fields[3].find_all('strong')[1].next_sibling.strip()
            )  # offense text
        else:
            data['charge'] = ''
        if id_and_type['record_type'] == 'Arrest':
            data['name'] = record_fields[3].find_all('strong')[0].next_sibling.strip()  # arrestee
            id_and_type['record_id'] = hashlib.sha224(data['name'] + data['occurred_date'] + data['address']
                 + data['charge']).hexdigest()
            other_data['id_generate'] = '1'
        else:
            if len(record_fields[3].find_all('strong')) == 0:
                id_and_type['record_id'] = hashlib.sha224(data['occurred_date'] + data['address']).hexdigest()
            else:
                id_and_type['record_id'] = record_fields[3].find_all('strong')[0].next_sibling.strip()  # case number
        # geocoded = bing_geocode.geocode(new_record[5] + ', NC')
        # if geocoded['geocoded']:
        #     new_record[5] = geocoded['address']
        #     new_record[6] = geocoded['city']
        #     new_record[7] = geocoded['county']
        #     new_record[8] = geocoded['state']
        #     new_record[9] = geocoded['zip_code']
        #     new_record[10] = geocoded['lat']
        #     new_record[11] = geocoded['lon']
#this is to download the pdf. not sure if we want to try that now.
#        data['pdf'] = dl_pdf(record_fields[5].find('a')['href'].strip().split("'")[1], data['record_id'],
#                                v_e)  # pdf stuff, but this isn't going to help us right now

        data = dict(data.items() + other_data.items() + id_and_type.items() + {'agency': agency}.items())
        scraper_commands.all_data[id_and_type['record_type']].append(scraper_commands.check_data(data))


def dl_pdf(target, record_id, v_e):
    if target == '' or target is None:
        return ''
    global search_items, url, date_range, community_item
    pdf_search_items = search_items
    pdf_search_items['__EVENTTARGET'] = target
    pdf_search_items['__EVENTARGUMENT'] = ''
    payload = dict(pdf_search_items.items() + v_e.items() + date_range.items() + community_item.items())
    referer = {'Referer': url}
    pdf_response = s.post(url, data=payload, headers=referer, allow_redirects=True, stream=True)
    file_name = record_id + '.pdf'
    with open(file_name, 'wb') as out_file:
        shutil.copyfileobj(pdf_response.raw, out_file)
    del pdf_response
    return file_name


#parse ints
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def has_records(soup):
    if (len(soup.find_all('span', id='mainContent_lblRecordCount')) > 0):
        return True
    return False


#disclaimer
def pass_disclaimer(url):
    global disclaimer_items, search_items
    page = s.get(url)
    if page.url != url:
        disclaimer_url = page.url
        soup = BeautifulSoup(page.text)
        redirect_link = \
            soup.find_all('select', id="DDLSiteMap1_ddlQuickLinks")[0].find_all('option',
                                                                        attrs={'selected': "selected"})[0]['value']
        disclaimer_items['ctl00$MasterPage$DDLSiteMap1$ddlQuickLinks'] = redirect_link
        search_items['MasterPage$DDLSiteMap1$ddlQuickLinks'] = redirect_link
        v_e = find_v_e(page.text)
        payload = dict(v_e.items() + disclaimer_items.items())
        referer = {'Referer': disclaimer_url}
        page = s.post(disclaimer_url, data=payload, headers=referer)
    types_available(page)
    return page


#initial search page
def fetch_page(url, page, page_number, community, code, agency):
    global pages_of_records, date_range, community_item, search_items
    community_item['MasterPage$mainContent$CGeoCityDDL12'] = code
    soup = BeautifulSoup(page.text)
    v_e = find_v_e(page.text)
    if page_number > 1:
        search_items['__EVENTARGUMENT'] = 'Page$' + str(page_number)
        search_items['__EVENTTARGET'] = 'MasterPage$mainContent$gvSummary'
    else:
        search_items['__EVENTTARGET'] = 'MasterPage$mainContent$cmdSubmit2'
        search_items['__EVENTARGUMENT'] = ''

    payload = dict(search_items.items() + v_e.items() + date_range.items() + community_item.items())
    referer = {'Referer': url}
    page = s.post(url, data=payload, headers=referer)
    soup = BeautifulSoup(re.sub("\r", "\n", page.text.encode('utf-8')))
    v_e = find_v_e(page.text)
    if not has_records(soup):
        return
    if page_number == 1:
        pages_of_records = number_of_pages(soup)
    records = find_records(soup, community, agency)
    page_number += 1
    if page_number <= pages_of_records:
        fetch_page(url, page, page_number, community, code, agency)

def start_scrape(agency, url, howfar, county):
    global date_range
    global communities
    page = pass_disclaimer(url)
    communities = find_communities(page.text, county)
    date_ranges = make_date_ranges(howfar)
    for current_date_range in date_ranges:
        date_range = current_date_range
        for community, code in communities.items():
            fetch_page(url, page, 1, community, code, agency)
    return scraper_commands.all_data

