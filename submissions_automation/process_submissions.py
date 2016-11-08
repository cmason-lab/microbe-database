#!/usr/bin/env python3

import os

# Import all configuration variables from config.py; includes logging
from config import *

# ------------------------- ITERATE OVER UNPROCESSED SUBMISSIONS

# Go through an individual xlsx file and update the master 
def process_workbook( file_path ):
    print(file_path)

# Loop through all submissions in UNPROCESSED_SUBMISSIONS_DIR
for subdirs, dirs, files in os.walk(UNPROCESSED_SUBMISSIONS_DIR):
    for filename in files:
        file_path = '{}{}'.format(UNPROCESSED_SUBMISSIONS_DIR, filename)
        process_workbook(file_path)
        # Move the file from unprocessed to processed
        #os.rename(file_path, '{}{}'.format(PROCESSED_SUBMISSIONS_DIR, filename))