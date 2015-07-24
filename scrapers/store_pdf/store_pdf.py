import os
import shutil
from slugify import slugify
from scraper_config import make_config


home_dir, data_dir, database, db_user, db_pw, commands_url = make_config()
parent_dir = home_dir + 'pdfs'

def store_file(pdf_response, path_to_file):
    if file_exists(path_to_file):
        return path_to_file
    with open(path_to_file, 'wb') as out_file:
        shutil.copyfileobj(pdf_response.raw, out_file)
        del pdf_response
    return path_to_file


def create_file_name(record_id, record_type, agency):
    directory = '/'.join([parent_dir,slugify(agency)])
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = '/'.join([directory,record_type])
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = record_id + '.pdf'
    return '/'.join([directory,file_name])

def file_exists(path_to_file):
    if os.path.exists(path_to_file):
        return True
    return False

