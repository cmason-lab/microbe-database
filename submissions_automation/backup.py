#!/usr/bin/env python3

import dropbox

# This should be in a separate cron job and should only happen once a week or so
# Set up the connection to the dropbox

client = dropbox.client.DropboxClient(DROPBOX_ACCESS_TOKEN)
#f, metadata = client.get_file_and_metadata(ERROR_LOG)

# We need some sort of system to email people who did not make their weekly assignment

# Upload the modified log file to Dropbox
# You have to be careful w/ how many requests you send or dropbox will refuse your connection
#with open(TEMP_ERROR_LOG, 'r') as f:
    #client.put_file(ERROR_LOG, f, True)
    
# Also upload the error log to the dropbox
