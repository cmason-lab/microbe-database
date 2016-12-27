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
UNASSIGNED_ASSIGNMENTS_DIR = 'assignments/unassigned/'
ASSIGNED_ASSIGNMENTS_DIR = 'assignments/assigned/'
TEMPLATE_PATH = 'annotations_template.xlsx'
ANN_TO_ASSIGN_PATH = 'annotations_to_assign.xlsx'
SUBMITTERS_PATH = 'submitters.xlsx'

keys_to_cols = {'optimal_pH': 13, 'optimal_temperature': 15, 'pathogenicity': 19,
                'antimicrobial_susceptibility': 29, 'spore_forming': 49, 'biofilm_forming': 51,
                'extreme_environment': 3, 'gram_stain': 41, 'microbiome_location': 7, 'plant_pathogen': 33,
                'animal_pathogen': 35}

type_from_key = {'optimal_pH': 'range', 'optimal_temperature': 'range', 'pathogenicity': '1-4',
                'antimicrobial_susceptibility': 'binary', 'spore_forming': 'binary',
                'biofilm_forming': 'binary', 'extreme_environment': 'binary', 'gram_stain': '0-2',
                'microbiome_location': 'binary', 'plant_pathogen': 'binary', 'animal_pathogen': 'binary'}

# ------------------------- ERROR LOGGING

def log( msg ):
    with open(ERROR_LOG, 'a') as f:
        # Add a timestamp to the message
        time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        log_msg = '{}: {}\n'.format(time, msg)
        f.write(log_msg)
        print(log_msg)