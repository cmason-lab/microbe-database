#!/usr/bin/env python
# coding=utf-8

import openpyxl
import re

def validate(str, type):
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
        if pattern.match(value):
            print('{} is a valid {}.'.format(str, type))
            return True
        else:
            print('{} is not a valid {}'.format(str, type))
            return False
    else:
        print('{} is not defined.'.format(type))
        return False

path = 'annotations_master 12-19-16 - Copy.xlsx'
wb = openpyxl.load_workbook(filename=path)
ws = wb.get_active_sheet()

keys_to_cols = {'optimal_pH': 13, 'optimal_temperature': 15, 'pathogenicity': 19,
                'is_susceptible_to_antibiotics': 29, 'spore_forming': 49, 'biofilm_forming': 51,
                'is_extremophile': 3, 'gram_stain': 41, 'found_in_microbiome': 7}

type_from_key = {'optimal_pH': 'range', 'optimal_temperature': 'range', 'pathogenicity': '1-4',
                'is_susceptible_to_antibiotics': 'binary', 'spore_forming': 'binary',
                'biofilm_forming': 'binary', 'is_extremophile': 'binary', 'gram_stain': '0-2',
                'found_in_microbiome': 'binary', 'plant_pathogen': 'binary', 'animal_pathogen': 'binary'}

for row in range(2, ws.max_row+1):
    for key in keys_to_cols:
        col = keys_to_cols[key]
        type = type_from_key[key]
        
        value = str(ws.cell(row = row, column = col).value)
        
        if value == '#N/A' or value == 'N/A' or value =='None':
            continue
        
        if validate(value, type) is False:
            value = '{} badformat {}'.format(value, key)
            ws.cell(row = row, column = col).value = value

wb.save(path)