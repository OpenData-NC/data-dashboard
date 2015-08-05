#!/usr/bin/env python
import requests
#this holds our data as we gather it.
#each element of each array is a tab-delimited lines of data
all_data = {'Incident': [], 'Arrest': [], 'Accident': [], 'Citation': []}
#these are the fields we'll have in our database tables for each of these items
#some of them will be blank for some records because:
# * the data wasn't there when we pulled it
# * some records of the same type have different formats: e.g., date vs. datetime
# * we'll be adding it later, such as the path to the pdf or geocode info
required_fields = {
    'Incident': [
        'record_id', 'agency', 'name', 'age', 'race', 'sex', 'on_date', 'from_date'
        , 'to_date', 'reported_date', 'date_reported', 'time_reported', 'address', 'charge', 'offense_code', 'reporting_officer']
        ,
    'Accident': ['record_id', 'agency', 'name1', 'name2', 'occurred_date'
        , 'date_occurred', 'time_occurred', 'address', 'reporting_officer'
    ],
    'Arrest': [
        'record_id', 'agency', 'name', 'age', 'race', 'sex', 'occurred_date'
        , 'date_occurred', 'time_occurred', 'address', 'charge', 'offense_code'
        , 'reporting_officer'
    ],
    'Citation': [
        'record_id', 'agency', 'name','age', 'race', 'sex', 'occurred_date'
        , 'date_occurred', 'time_occurred', 'address', 'charge', 'reporting officer'
    ]
}
#these are added to required fields, are common to all

other_fields = ['pdf', 'street_address', 'city', 'county', 'state', 'zip', 'lat', 'lon', 'scrape_type', 'id_generate']

#this takes the data we scraped in the form of a dictionary and checks it for required field
#if that field isn't there, we add it as a blank. this also strips out spaces on either side of the fields
#then, we format it as a tab-delimited string and pass it back to add to that record type's array
def check_data(data):
    ordered_data = []
    required = required_fields[data['record_type']] + other_fields
    for field in required:
        if field not in data:
            data[field] = ''
        ordered_data.append(data[field].strip())
    return "\t".join(ordered_data)


#this takes our final collection of data, going through each data type to create a file name (e.g., arrest.txt)
#and printing out all of that data into the file. so we end up with a tab-delimited file for each record type.
#later we'll take these files and insert them into their tables.
def print_files(data,data_dir, site=''):
    for record_type, records in data.iteritems():
        holder = ''
        data_file = data_dir + '/' + site + record_type + '.txt'
        for record in records:
            holder = holder + record + "\n"
        with open(data_file, 'w') as f:
            f.write(holder.encode('utf8'))
            f.close()

#this fetches command parameters from the google spreadsheet.
#it returns an array of dictionaries with items such as the agency,
#url, city, county, how many days back to scrape.
#these are passed to either scrape_bulletin or scrape_search,
#depending on whether the site has a daily bulletin available
def fetch_commands(url=None):
    if url is None:
        print "No url passed to fetch commands."
    else:
        commands = []
        data = requests.get(url)
        lines = data.text.split("\n")
        headers = lines.pop(0).split(",")
        headers = [header.strip() for header in headers]
        for line in lines:
            pieces = line.split(",")
            pieces = [p.strip() for p in pieces]
            commands.append(dict(zip(headers, pieces)))
        return commands
