#!/usr/bin/env python3.5

import re
import csv

class SpeciesParser:
    def parse_humann(self, file_path):
        '''Parses humann2_pathabundance.tsv's'''
        
        species_list = []
        expr = re.compile('.*s__(.+)\t.*')
        
        with open(file_path, 'r') as f:
            for line in f:
                if expr.match(line):
                    species = re.sub(expr, '\\1', line)
                    species = species.replace('_', ' ')
                    species = species.replace('\n', '')
                    species_list.append(species)
        
        # Make sure we have no duplicates
        return set(species_list)
    
    def parse_metaphlan(self, file_path):
        species_list = []
        expr = re.compile('.*s__([^\t|]+)\t.*')
        
        with open(file_path, 'r') as f:
            for line in f:
                if expr.match(line):
                    species = re.sub(expr, '\\1', line)
                    species = species.replace('_', ' ')
                    species = species.replace('\n', '')
                    species_list.append(species)
        
        # Make sure we have no duplicates
        return set(species_list)
    
    def parse_clark(self, file_path):
        species_list = []
        
        firstLine = True
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                if firstLine is False:
                    species_list.append(line[0])
                firstLine = False
        
        # Make sure we have no duplicates
        return set(species_list)
    
    def species_query(self, species_set):
        species_query = ''
        
        last_index = len(species_set)-1
        for i, species in enumerate(species_set):
            print(species)
            print(species_query)
            print(len(species_query))
            species_query += "species='{}'".format(species)
            
            if i is not last_index:
                species_query += ' OR '     
        print(species_query)
        return species_query