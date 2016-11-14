import datetime

# ------------------------- CONFIGURATION

# Must turn on 'allow acess from less secure apps' in gmail settings
USERNAME = 'microbe.submissions@gmail.com'
PASSWORD = 'masonlab12345'
DROPBOX_ACCESS_TOKEN = 'BPQ7ih529eAAAAAAAAAAE1szjo_Z6waoj-_jCb7WQ0ctfH2yYkciB3925AKvS7Wk'
# The location of the error log (on the filesystem)
ERROR_LOG = 'error.log'
# This is a log file that contains the Message-ID of each emails we've processed
PROCESSED_EMAILS = 'processed_emails.csv'
# Where we are going to save the submissions
UNPROCESSED_SUBMISSIONS_DIR = 'submissions/unprocessed/'
PROCESSED_SUBMISSIONS_DIR = 'submissions/processed/'
MASTER_WS_PATH = 'annotations_master.xlsx'
ASSIGNMENTS_DIR = 'assignments\\'
TEMPLATE_PATH = 'annotations_template.xlsx'
ANN_TO_ASSIGN_PATH = 'annotations_to_assign.xlsx'

# ------------------------- ERROR LOGGING

def log( msg ):
    with open(ERROR_LOG, 'a') as f:
        # Add a timestamp to the message
        time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        log_msg = '{}: {}\n'.format(time, msg)
        f.write(log_msg)
        print(log_msg)