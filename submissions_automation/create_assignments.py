#!/bin/usr/env python3

import openpyxl
from config import *
import shutil
import math
import os

# How many people are working on this project
num_submitters = 10
# How many annotations does each person do per week?
annotations_per_week = 10

read_wb = openpyxl.load_workbook(filename = ANN_TO_ASSIGN_PATH)
read_ws = read_wb.get_active_sheet()

entries = []

for row in range(2, read_ws.max_row+1):
    full_taxonomy = read_ws.cell(row = row, column = 1).value
    genus_species = read_ws.cell(row = row, column = 2).value
    entries.append({'full_taxonomy': full_taxonomy, 'genus_species': genus_species})

# Splits the num of entries to be completed amongst all submitters
total_assignments = []
annotations_per_submitter = math.ceil(len(entries)/num_submitters)

for i in range(0, len(entries), annotations_per_submitter):
    annotations_for_submitter = entries[i:i+annotations_per_submitter]
    total_assignments.append(annotations_for_submitter)

# This is how many weeks it will take to complete this at 10/week
num_weeks = math.ceil(annotations_per_submitter/annotations_per_week)
print('It will take {} weeks for {} people to complete {} annotations/week'.format(num_weeks, num_submitters, annotations_per_week))

# This will be assignments[ID number][week number]
assignments = []

for i in range(0, num_submitters):
    assignments.append([])

    for j in range(0, num_weeks):
        assignments[i].append(total_assignments[i][j*annotations_per_week:j*annotations_per_week+annotations_per_week])

# Create a .xlsx for each week
for i in range(0, num_submitters):
    dir = '{}{}'.format(ASSIGNMENTS_DIR, i+1)
    # Remove the old dir if it exists
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    
    for j in range(0, num_weeks):
        assignment = assignments[i][j]
        assignment_name = '{}_{}'.format(i, j)
        # This is the filename of the assignment's xlsx
        assignment_xlsx = '{}\\{}\\{}.xlsx'.format(ASSIGNMENTS_DIR, i+1, assignment_name)
        
        # Copy the template (do this to preserve formatting)
        shutil.copyfile(TEMPLATE_PATH, assignment_xlsx)
        
        # Edit the template you just copied
        write_wb = openpyxl.load_workbook(filename = assignment_xlsx)
        write_ws = write_wb.get_active_sheet()
        
        # Start filling things in at row 2
        row = 2
        
        for entry in assignment:
            full_taxonomy = entry['full_taxonomy']
            genus_species = entry['genus_species']
            
            write_ws.cell(row = row, column = 1).value = full_taxonomy
            write_ws.cell(row = row, column = 2).value = genus_species
            row = row + 1

        # Save the changes
        write_wb.save(assignment_xlsx)
