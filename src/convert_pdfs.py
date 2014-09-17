#!/usr/bin/env python

import glob
import os
from subprocess import call

home_dir = '/home/vaughn.hagerty/crime-scrapers/'
pdfs_dir = home_dir + 'pdfs'


#TODO: poss. use qpdf to unencrypt those that are before converting?
#initial tests show this may be unnecessary
def pdf_to_text(incident_type):
    files = glob.glob(incident_type + '/*.pdf')
    for pdf_file in files:
        text_file = pdf_file.replace('pdf','txt')
        if os.path.exists(text_file):
            continue
        command = 'pdftotext -layout ' + pdf_file + ' ' + text_file
        print command
        call(command,shell=True)


def check_dir(directory):
    directory = directory.replace('pdf','txt')
    if not os.path.exists(directory):
        os.makedirs(directory)


agencies = glob.glob(pdfs_dir + '/*')
for agency in agencies:
    check_dir(agency)
    incident_types = glob.glob(agency + '/*')
    for incident_type in incident_types:
        check_dir(incident_type)
        pdf_to_text(incident_type)

