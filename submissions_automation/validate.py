import re

def validate(str, type):
    lower = str.lower()
    if lower == '#n/a' or lower == 'n/a' or lower == 'na' or lower =='none':
        return False
    
    if type == 'range':
        # This won't work if the number has a leading decimal. Decimal numbers should have a leading 0
        pattern = re.compile('^((-?[0-9]+\.?[0-9]*)([:](-?[0-9]+\.?[0-9]*))?)(,((-?[0-9]+\.?[0-9]*)([:](-?[0-9]+\.?[0-9]*))?))*$')
    elif type == 'binary':
        pattern = re.compile('^[01]$')
    elif type == '1-4':
        pattern = re.compile('^[1-4]$')
    elif type == '0-2':
        pattern = re.compile('^[0-2]$')
    
    if pattern:
        if pattern.match(str):
            #print('{} is a valid {}.'.format(str, type))
            return True
        else:
            #print('{} is not a valid {}'.format(str, type))
            return False
    else:
        #print('{} is not defined.'.format(type))
        return False