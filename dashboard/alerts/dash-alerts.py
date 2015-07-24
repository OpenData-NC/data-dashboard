#!/usr/bin/env python

#script to check if any new data has been collected that matches a query the user has saved
#we use SendGrid, so you'll need to set up an account there. The free tier is allows something
#like 25K/mo., so it should be adequate for most cases.
#we use the same rEST API as the dashboard search. the data we store for the alerts is used to build the
#the query url and data is returned as json.
#if we find new data, we'll format it into a table and send an email -- one email per user/day, regardless of the number of alerts
#that user has saved.
#NOTE: This is only searching crime data at this point, in large part because the other data isn't updated more than once a month.
#in addition, "new data" means data that's new to the database. Each scrape looks for recent data *and* for data that's older than the
#oldest data currently in the database for that agency. we do this to gather historic data as well.
#each record gets timestamped when it enters our database. that timestamp is used by the alert system to determine whether
#data is new -- whether it entered the database after the last time we searched as part of the alert system.

import MySQLdb
import datetime
import requests
import sendgrid
import json
import jinja2

from alert_config import make_config

base_url, sg_user, sg_pw, email_template_dir, results_template_file, email_template_file, db, host, db_user, db_pw, insert_user, insert_pw = make_config()

#to send email alerts
sg = sendgrid.SendGridClient(sg_user, sg_pw)


select_connection = MySQLdb.connect(user=user, passwd=pw, db=db, host=host)
select_cursor = select_connection.cursor()
#for updates
insert_connection = MySQLdb.connect(user=insert_user, passwd=insert_pw, db=db, host=host)
insert_cursor = insert_connection.cursor()

#templates to format results for emails
template_loader = jinja2.FileSystemLoader( email_template_dir )
template_env = jinja2.Environment( loader=template_loader )
results_template = template_env.get_template( results_template_file )
email_template = template_env.get_template( email_template_file )

#update last searched so next run will get subsequent data
def update_last_searched():
    sql = 'update dash_alerts set last_searched = now()'
    insert_cursor.execute(sql)
    insert_connection.commit()

#we use our rest api to search
def search_data(query):
    query_url = base_url + query[2] + '|last-searched|' + query[1]
    results = requests.get(query_url)
    #flag to let us know if we have any results
    success = False
    formatted_results = ''
    try:
        data = json.loads(results.text)['results']
    except:
        #some sort of problem if it's not json, so let's just return
        return False
    for data_type in data:
        #if there's an element in this array, format it for return
        if len(data[data_type]['data']) > 0:
            formatted_results += format_results(data[data_type]['data'], data[data_type]['headings'], data_type, query[2], query[1])
            success = True
    if not success:
        return False
    return formatted_results
    

#we'll format the results into an html table
def format_results(data, headings, data_type, query, last_searched):
    #we'll use the search url to remind the user what was searched for
    #this formats them into an unordered list like this Field: search string
    query_params = query.replace('/search/','').split('|')
    dashboard_url = make_dashboard_url(query, query_params[1], last_searched, data_type)
    formatted_query_params = []
    for i in range(0, len(query_params)):
        formatted_param = query_params[i]
        if i%2 == 0:
            formatted_param = formatted_param.replace('_', ' ')
            formatted_param = formatted_param.replace('-', ' ')
            formatted_param = '<li><strong>' + formatted_param.capitalize() + ':</strong> '
        else:
            formatted_param+= '</li>'
            
        #need titlecase
        formatted_query_params.append(formatted_param)
    search = ''.join(formatted_query_params)
    #these fields won't be in our return results because they only work/are relevant to the web dashboard
    del_headings = ['Record ID']
    #we'll filter out the headings and use the indexes of the filtered headings to filter each row of data as well
    del_indexes = []
    filtered_data = []
    for i in range(0, len(headings) -1):
        if headings[i] in del_headings:
            del_indexes.append(i)
            del headings[i]
    for row in data:
        for i in del_indexes:
            del row[i]
            filtered_data.append(row)
    final_data = format_pdfs(filtered_data)
    #this dictionary is passed to the template. headings becomes the headings of the table 
    #and each element (row) of filtered_data becomes a table row 
    template_data = {'data_type': data_type, 'search': search, 'headings': headings, 'rows': final_data, 'dashboard_url': dashboard_url}
    return results_template.render( template_data )


def make_dashboard_url(query, county, last_searched, data_type):
    county = county.replace(' ', '-')
    data_type = data_type.replace(' ', '-')
    return base_url + '/' + county + '/search/' + data_type + '/#!' + query + '|last-searched|' + last_searched 

    
def format_pdfs(data):
    final_data = []
    for row in data:
        final = len(row) -1
        if row[final].find('pdf') != -1:
            row[final] = '<a href="{}">PDF report</a>'.format(row[final].replace('/home/vaughn.hagerty/crime-scrapers','http://pdf.open-nc.org'))
        final_data.append(row)
    return final_data


#use sendgrid's api to send the email    
def send_alerts(name, email, results):
    email_data = {'name': name, 'results': results}
    email_body = email_template.render( email_data )
    to_email = '{} <{}>'.format(name, email)
    message = sendgrid.Mail()
    message.add_to(to_email)
    message.set_subject('Open N.C. data alert') #let's add a date here
    message.set_html(email_body)
    message.set_from(from_email)
    status, msg = sg.send(message)

#get all of our active alerts, along with the users' names
def fetch_alerts():
    sql = 'select a.email `email`, last_searched, search, name from dash_alerts a inner join dash_users b on a.email = b.email where active = 1 order by a.email'
    select_cursor.execute(sql)
    result = select_cursor.fetchall()
    #we want them all as strings, mainly because python mysql returns date fields as date objects
    #we need them as strings
    return [[str(val) for val in row] for row in result]


#utility function to group the alerts by user email so we can send one email for all of a user's alert.
#it's a dictionary like this {'user@email.com':[[alert1],[alert2]], ... }
def organize_alerts(alerts):
    email = ''
    alerts_by_user = {}
    for alert in alerts:
        if email != alert[0]:
            email = alert[0]
            alerts_by_user[email] = []
        alerts_by_user[alert[0]].append(alert)
    return alerts_by_user


def main():
    #a dictionary of each users' alerts. see organize_alerts above
    alerts = organize_alerts(fetch_alerts())
    name = ''
    for email in alerts:
        #used to hold any successful searches
        records_found = []
        for search_query in alerts[email]:
            name = search_query[3]
            search_results = search_data(search_query)
            if search_results:
                records_found.append(search_results)
        #if we have any successful searches, we'll send them as one email
        if len(records_found) > 0:
            send_alerts(name, email, "\n".join(records_found))
    #update all of the alerts with the current date, which we'll use the following day to find any new data
    update_last_searched()

if __name__ == '__main__':
    main()