#!/usr/bin/env python3

import imaplib
import email
import sys
import os

import email_assistant

# Import all configuration variables from config.py; includes logging
from config import *

# ------------------------- CONNECT TO GMAIL

# Must enable imap in gmail settings
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(USERNAME, PASSWORD)

# ------------------------- SEARCH FOR UNPROCESSED EMAILS

# All emails automatically go to 'Unprocessed' (via gmail filters)
mail.select('Unprocessed')
response, data = mail.search(None, 'ALL')
# Email ids are underscore-delimited and reside at data[0]
unprocessed_email_ids = data[0].split()

# Exit the script if there's nothing to process
if len(unprocessed_email_ids) == 0:
    exit()

# ------------------------- PROCESS EACH EMAIL

# Fxn that gets a python representation of the raw email from the server
def get_email_by_id( email_id ):
    # Get the raw data of the email
    response, data = mail.fetch(email_id, "(RFC822)")
    # The raw message is in the data arrray at [0][1], not sure why... 
    return email.message_from_bytes(data[0][1])

def change_email_label( email_id, label ):
    # Add the new label
    mail.copy(email_id, label)
    # Delete the old label
    mail.store(email_id , '+FLAGS', '(\Deleted)')
    mail.expunge()

for email_id in unprocessed_email_ids:
    email_msg = get_email_by_id(email_id)
    
    # Parse the emails by subject to see what was submitted
    subject = email_msg['Subject']
    
    # Subject line is formatted as {Submitter ID} {Week #}
    # Try to parse this. If there's an error, write this in the log
    try:
        subject_split = subject.split('_')
        submitter_id = subject_split[0];
        submission_week = subject_split[1];
    except:
        # Record the error
        log('SUBJECT of email {} is formatted incorrectly.'.format(email_msg['Message-ID']))
        # Move the email from 'Unprocessed' to 'Error'
        change_email_label(email_id, 'Error')
        
        # Skip further processing of this email
        continue
    
    submitter_email = email_msg['From']
    submit_date = email_msg['Date']
    
    has_attachment = False
    
    # Pull out and save the attachment
    if email_msg.is_multipart():
        for part in email_msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            extension = os.path.splitext(filename)[1]
            
            if filename is not None:
                # This is where we will save/download the attached submission; same as subject but w/ .xlsx extension
                submission_save_path = os.path.join(UNPROCESSED_SUBMISSIONS_DIR, '{}.xlsx'.format(subject))
                
                # Make sure the file doesn't already exist and that it's a .xslx
                if not os.path.isfile(submission_save_path) and extension == '.xlsx':
                    # Save the attachment
                    with open(submission_save_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                        has_attachment = True
                else:
                    log('Error saving attachment, {}, for email {}. File already exists and/or is not a .xlsx file'.format(submission_save_path, email_msg['Message-ID']))
                    # Move the email from 'Unprocessed' to 'Error'
                    change_email_label(email_id, 'Error')
    
    # Log an error if we can't find an attachment
    if has_attachment is not True:
        log('No attachment found for email {}.'.format(email_msg['Message-ID']))
        # Move the email from 'Unprocessed' to 'Error'
        change_email_label(email_id, 'Error')
    
    # Move the email from 'Unprocessed' to 'Processed'
    change_email_label(email_id, 'Processed')
    
    # Send out their new assignement
    asst = email_assistant.EmailAssistant(USERNAME, PASSWORD)
    #asst.send_email('david@reflashed.com', 'SUBJECT TEST', 'test', ['file1.png', 'file2.png'])