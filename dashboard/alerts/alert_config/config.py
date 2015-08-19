#!/usr/bin/env python

#change these to match your values
def make_config():
    #used to make queries to api
    base_url = 'http://data.open-nc.org'

    #to send email alerts
    sg_user = '[your sendgrid username]'
    sg_pw = '[your sendgrid password'
    from_email = '[email address for "from" header'
    
    #directory where our jinja templates are stored
    email_template_dir = '[your template director here]'
    results_template_file = "results.jinja"
    email_template_file = "email.jinja"

    #db config
    db = '[database name]'
    #set this to localhost or the ip of your database if not on the same server
    host = '[host]'

    #this user only has select permissions
    db_user = '[db user with select permissions on database]'
    db_pw = '[select pw]'
    #used to update alert info
    insert_user = '[db user with select, insert, update permissions on alert tables]'
    insert_pw = '[insert user pw]'

   return (base_url, sg_user, sg_pw, email_template_dir, results_template_file, email_template_file, db, host, db_user, db_pw, insert_user, insert_pw)
