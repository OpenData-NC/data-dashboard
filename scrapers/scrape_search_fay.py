import datetime
import requests
from bs4 import BeautifulSoup
import re
import hashlib

import scraper_commands
import date_formatters
import store_pdf


disclaimer_items = {'_popupBlockerExists': 'true', '__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '',
                    'ctl00$MasterPage$DDLSiteMap1$ddlQuickLinks': '~/main.aspx',
                    'ctl00$MasterPage$mainContent$CenterColumnContent$btnContinue': 'I Agree'}
search_items = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '',
                    'MasterPage$DDLSiteMap1$ddlQuickLinks': '~/redirect.aspx?pg=fpdhome', 'MasterPage$mainContent$txtCase2': '',
                    'MasterPage$mainContent$rblSearchDateToUse': 'Date Reported',
                    'MasterPage$mainContent$ddlDates': 'Specify Date', 'MasterPage$mainContent$txtLName': '',
                    'MasterPage$mainContent$txtFName': '', 'MasterPage$mainContent$txtMName': '',
                    'MasterPage$mainContent$txtStreetNo': '', 'MasterPage$mainContent$txtStreetName': '',
                    'MasterPage$mainContent$ddlNeighbor': '', 'MasterPage$mainContent$ddlRange': '',
                    'MasterPage$mainContent$addresslat': '', 'MasterPage$mainContent$addresslng': ''}

community_item = {'MasterPage$mainContent$CGeoCityDDL11': ''}  # testing

s = requests.Session()
county_st = ''

def find_range(farback, start_date = 0):
#    date_wanted = (datetime.datetime.today() - datetime.timedelta(days=farback)).strftime('%m/%d/%Y')
    if not start_date:
        start_date = datetime.datetime.today()
    date_wanted = (start_date - datetime.timedelta(days=farback)).strftime('%m/%d/%Y')
    return {'MasterPage$mainContent$txtDateFrom$txtDatePicker': date_wanted, 'MasterPage$mainContent$txtDateTo$txtDatePicker': date_wanted}

#def make_date_ranges(howfar):
#    date_ranges = []
#    while howfar >= 0:
#        date_ranges.append(find_range(howfar))
#        howfar -= 1
#    return date_ranges
def make_date_ranges(agency, howfar = 0):
    print agency
    howfar_save = howfar
    min_date = date_formatters.find_min_date(agency)
    date_ranges = []
    while howfar >= 0:
        date_ranges.append(find_range(howfar))
        if min_date:
            date_ranges.append(find_range(howfar,min_date))
        howfar -= 1
    return date_ranges



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


# remove the stray semicolon beautiful soup adds
def remove_semicolon(text):
    return re.sub(r';$', '', text)


#extract communities
def find_communities(page, county='None'):
    communities_available = {}
    soup = BeautifulSoup(page)
    if len(soup.find_all("select", {'class':"geofields2"})) > 0:
        options = soup.find_all("select", {'class':"geofields2"})[0].find_all("option")
    elif soup.find_all("select", class_="geofields") > 0:
        options = soup.find_all("select", {'class':"geofields"})[0].find_all("option")
    else:
        return communities_available
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
def find_records(soup, community, agency, county, url):
    global date_range
    records = soup.find_all('tr', {'class':'EventSearchGridRow'})
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
        data['occurred_date'] = date_formatters.format_db_datetime(record_fields[1].string.strip())  # date
        data['address'] = re.sub(r' +', ' ', record_fields[4].string.strip())
        if re.search('[A-Za-z]+',data['address']) is not None:
            data['address'] = data['address'] + county_st
        if id_and_type['record_type'] == 'Incident':
            data['reported_date'] = date_formatters.format_db_date(date_range['MasterPage$mainContent$txtDateFrom$txtDatePicker'])
            data['date_reported'] = data['reported_date']
            data['time_reported'] = ''
            data['on_date'] = data['occurred_date']
        else:
            data['date_occurred'] = date_formatters.format_db_date_part(record_fields[1].string.strip())
            data['time_occurred'] = date_formatters.format_db_time_part(record_fields[1].string.strip()) 
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
#this is to download the pdf. not sure if we want to try that now.
        has_gif = record_fields[5].find('a').find('div')
        if has_gif is None:
            #there's no pdf
            #return ''
            data['pdf'] = ''
        else:
            data['pdf'] = dl_pdf(record_fields[5].find('a')['href'].strip().split("'")[1], id_and_type,
                                    agency, v_e, url)  # pdf stuff

        data = dict(data.items() + other_data.items() + id_and_type.items() + {'agency': agency, 'county': county}.items())
        scraper_commands.all_data[id_and_type['record_type']].append(scraper_commands.check_data(data))


def dl_pdf(target, id_and_type, agency, v_e, url):
    if target == '' or target is None:
        return ''
    pdf_file = store_pdf.create_file_name(id_and_type['record_id'],id_and_type['record_type'],agency)
    if store_pdf.file_exists(pdf_file):
        return pdf_file
    global search_items, date_range, community_item
    pdf_search_items = search_items
    pdf_search_items['__EVENTTARGET'] = target
    pdf_search_items['__EVENTARGUMENT'] = ''
    payload = dict(pdf_search_items.items() + v_e.items() + date_range.items() + community_item.items())
    referer = {'Referer': url}
    try:
        pdf_response = s.post(url, data=payload, headers=referer, allow_redirects=True, stream=True)
    except requests.exceptions.ConnectionError as e:
        return ''
    pdf_file = store_pdf.store_file(pdf_response,pdf_file)
    return pdf_file


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
def fetch_page(url, page, page_number, community, code, agency, county):
    global pages_of_records, date_range, community_item, search_items
    community_item['MasterPage$mainContent$CGeoCityDDL11'] = code
    soup = BeautifulSoup(page.text)
    v_e = find_v_e(page.text)
    if page_number > 1:
        search_param = {}
        search_items['__EVENTARGUMENT'] = 'Page$' + str(page_number)
        search_items['__EVENTTARGET'] = 'MasterPage$mainContent$gvSummary'
    else:
        search_param = {'MasterPage$mainContent$cmdSubmit': 'Search'}
        search_items['__EVENTTARGET'] = ''
        search_items['__EVENTARGUMENT'] = ''
    payload = dict(search_items.items() + v_e.items() + date_range.items() + community_item.items() + search_param.items())
    referer = {'Referer': url}
#    page = s.post(url, data=payload, headers=referer)
    try:
        page = s.post(url, data=payload, headers=referer)
    except requests.exceptions.ConnectionError as e:
        page_number += 1
        if page_number <= pages_of_records:
            fetch_page(url, page, page_number, community, code, agency, county)
        else:
            return
    soup = BeautifulSoup(re.sub("\r", "\n", page.text.encode('utf-8')))
    v_e = find_v_e(page.text)
    if not has_records(soup):
        return
    if page_number == 1:
        pages_of_records = number_of_pages(soup)
    records = find_records(soup, community, agency, county, url)
    page_number += 1
    if page_number <= pages_of_records:
        fetch_page(url, page, page_number, community, code, agency, county)


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
            assert(len(selected_options) < 2)
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]
        
        fields[select['name']] = value
    
    return fields

def start_scrape(agency, url, howfar, county):
    global date_range
    global communities
    global county_st
    if county.find('County') == -1:
        county_st = ', ' + county + ' County, NC'
    else :
        county_st = ', ' + county + ', NC'
    page = pass_disclaimer(url)
    communities = find_communities(page.text, county)
    date_ranges = make_date_ranges(agency, howfar)
    for current_date_range in date_ranges:
        date_range = current_date_range
        for community, code in communities.items():
            fetch_page(url, page, 1, community, code, agency, county)
    return scraper_commands.all_data

