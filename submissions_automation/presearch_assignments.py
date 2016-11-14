#!/Users/David/AppData/Local/Programs/Python/Python35-32/python

import os
import annotations_automator

# Import all configuration variables from config.py; includes logging
from config import *

def presearch_assignment(file_path):
    automator = annotations_automator.AnnotationsAutomator(file_path)
    automator.search_MicrobeWiki()
    #automator.search_BacMap()
    #automator.search_ATCC()
    #automator.search_VFDB()
    #automator.search_PATRIC()
    #automator.search_ARDB()
    #automator.search_GOLD()
    #automator.search_HOMD()
    #automator.search_BEI()
    automator.save_results()

# Loop through all submissions in UNPROCESSED_SUBMISSIONS_DIR
for subdir, dirs, files in os.walk(ASSIGNMENTS_DIR):
    for file in files:
        file_path = os.path.join(subdir, file)
        extension = os.path.splitext(os.path.basename(file_path))[1]
        
        if extension == '.xlsx':
            presearch_assignment(file_path)