#!/usr/bin/env python3.5
# coding=utf-8

# Tested with Python 3.5.2

import os
import shutil

import microbedb
import speciesparser
import visualizer

# Parse humann
HUMANN_INPUT_PATHS = ['humann/A4.humann2_pathabundance.tsv', 'humann/F2.humann2_pathabundance.tsv', 'humann/H9.humann2_pathabundance.tsv']
METAPHLAN_INPUT_PATHS = ['metaphlan/A4_S26.metaphlan2.tsv']
OUTPUT_PATH = 'output'

microbe_db = microbedb.MicrobeDB('microbe.db')
species_parser = speciesparser.SpeciesParser()

# Make the output dir
if os.path.isdir(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)

METAPHLAN_INPUT_DIR = 'metaphlan'
CLARK_INPUT_DIR = 'clark'

# Search the input dir
for (root, dirs, files) in os.walk(CLARK_INPUT_DIR):
    for path in files:
        input_path = CLARK_INPUT_DIR + '/' + path
        bn = os.path.basename(path)
        sample_name = os.path.splitext(bn)[0]
        
        # This var is kind of redundant
        save_name = '{}/{}/{}'.format(OUTPUT_PATH, sample_name, sample_name)
        
        # Make an output dir for the sample
        os.mkdir(OUTPUT_PATH + '/{}'.format(sample_name))
        
        #species_set = species_parser.parse_humann(path)
        species_set = species_parser.parse_clark(input_path)
        species_query = species_parser.species_query(species_set)
        
        print('Hi:')
        print(save_name)
        print(species_query)
        print(' ')
        
        if species_query is not '':
            binary_results = microbe_db.binary_counts(species_query)
            pathogenicity_results = microbe_db.pathogenicity_counts(species_query)
            gram_stain_results = microbe_db.gram_stain_counts(species_query)
            optimal_pHs = microbe_db.optimal_pH_data(species_query)
            optimal_temps = microbe_db.optimal_temp_data(species_query)
            
            visualizer.plot_booleans(binary_results, save_name)
            visualizer.plot_pathogenicity(pathogenicity_results, save_name)
            visualizer.plot_gram_stain(gram_stain_results, save_name)
            visualizer.plot_range(optimal_pHs, 'Optimal pH', 'Optimal pH', 'optimal_pH', save_name)
            visualizer.plot_range(optimal_temps, 'Optimal Temperature', 'Optimal Temperature (°C)', 'optimal_temperature', save_name)