__author__ = 'vaughn'
import datetime
import os
from scraper_config import make_config


home_dir, data_dir, database, db_user, db_pw, commands_url = make_config()

log_dir = home_dir + 'logs/'


def log(agency,msg):
    log_file = log_dir + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    log_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = "\t".join([agency, msg, log_date]) + "\n"
    if not os.path.exists(log_file):
        open_param = 'w'
    else:
        open_param = 'a'
    with open(log_file, open_param) as log:
        log.write(log_msg)
        log.close()
