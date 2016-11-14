#!/usr/bin/env python3

import os
import annotations_processor

# Import all configuration variables from config.py; includes logging
from config import *

# ------------------------- ITERATE OVER UNPROCESSED SUBMISSIONS

MASTER_WS_PATH = 'annotations_master.xlsx'

# Go through an individual xlsx file and update the master 
def process_workbook( file_path ):
    proc = annotations_processor.AnnotationsProcessor(file_path, MASTER_WS_PATH)
    proc.update()
    proc.save()

# Loop through all submissions in UNPROCESSED_SUBMISSIONS_DIR
for subdirs, dirs, files in os.walk(UNPROCESSED_SUBMISSIONS_DIR):
    for filename in files:
        file_path = '{}{}'.format(UNPROCESSED_SUBMISSIONS_DIR, filename)
        process_workbook(file_path)
        # Move the file from unprocessed to processed
        os.rename(file_path, '{}{}'.format(PROCESSED_SUBMISSIONS_DIR, filename))