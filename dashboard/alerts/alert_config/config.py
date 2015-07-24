#!/usr/bin/env python

#change these to match your values
def make_config():
    #used to make queries to api
    base_url = 'http://data.open-nc.org'

    #to send email alerts
    sg_user = 'opennc'
    sg_pw = 'send0pengr!dNC'
    from_email = 'Open N.C. Dashboard Alerts <dash@open-nc.org>'
    
    #directory where our jinja templates are stored
    email_template_dir = '/home/vaughn.hagerty/alerts/jinja-templates'
    results_template_file = "results.jinja"
    email_template_file = "email.jinja"

    #db config
    db = 'crime'
    #set this to localhost or the ip of your database if not on the same server
    host = '10.240.220.181'

    #this user only has select permissions
    db_user = 'dataDa5h'
    db_pw = 'UnC0p3n'
    #used to update alert info
    insert_user = 'crimeloader'
    insert_pw = 'redaolemirc'

   return (base_url, sg_user, sg_pw, email_template_dir, results_template_file, email_template_file, db, host, db_user, db_pw, insert_user, insert_pw)
