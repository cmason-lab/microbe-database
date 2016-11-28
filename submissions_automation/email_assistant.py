#!/usr/bin/env python3

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from os.path import basename

class EmailAssistant():
    ''' Connect to gmail and provide various functionality

Move and process xlsx files by column and organism name'''

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(self.username, self.password)
        
    def send_email(self, email_recipient, email_subject, email_message, attachments=[]):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = email_recipient
        msg['Subject'] = email_subject
        
        body = email_message
        msg.attach(MIMEText(body, 'plain'))
        
        for attachment in attachments:
            print(attachment)
            with open(attachment, 'rb') as f:
                part = MIMEApplication(
                    f.read(),
                    Name=basename(attachment)
                )
                part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attachment))
                msg.attach(part)
                   
        self.smtp.sendmail(self.username, email_recipient, msg.as_string())