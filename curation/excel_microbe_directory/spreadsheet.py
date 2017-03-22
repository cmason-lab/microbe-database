import openpyxl
import sqlite3
import os
import re

from . import cell_validator_factory

class Spreadsheet():
    _COLUMNS = {
        'optimal_pH': {
            'column': 13,
            'validation_type': 'range',
            'sql_type': 'TEXT'
        },
        'optimal_temperature': {
            'column': 15,
            'validation_type': 'range',
            'sql_type': 'TEXT'
        },
        'pathogenicity': {
            'column': 19,
            'validation_type': 'cogem_pathogenicity',
            'sql_type': 'INTEGER'
        },
        'antimicrobial_susceptibility': {
            'column': 29,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'spore_forming': {
            'column': 49,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'biofilm_forming': {
            'column': 51,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'extreme_environment': {
            'column': 3,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'gram_stain': {
            'column': 41,
            'validation_type': 'ternary',
            'sql_type': 'INTEGER'
        },
        'microbiome_location': {
            'column': 7,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'plant_pathogen': {
            'column': 33,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        },
        'animal_pathogen': {
            'column': 35,
            'validation_type': 'binary',
            'sql_type': 'INTEGER'
        }
    }
    
    def __init__(self, spreadsheet_path):
        self.spreadsheet_path = spreadsheet_path
        
        wb = openpyxl.load_workbook(filename = spreadsheet_path)
        self.ws = wb.get_active_sheet()
    
    def export_as_dictionary(self):
        ''' openpyxl worksheet --> python dictionary '''
        
        dict = {}
        
        for row in range(2, self.ws.max_row+1):
            species = self.ws.cell(row = row, column = 2).value
            dict[species] = {}
            
            taxa = self.__split_taxonomy_string(self.ws.cell(row = row, column = 1).value)
            taxa_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
            
            for i,taxa_level in enumerate(taxa_levels):
                dict[species][taxa_level] = taxa[i]
        
            # Add the other values from the spreadsheet
            for key in Spreadsheet._COLUMNS:
                column = Spreadsheet._COLUMNS[key]
                value = str(self.ws.cell(row=row, column=column['column']).value)
                
                if self.validate_cell(value, column['validation_type']):
                    dict[species][key] = value
        
        self.dict = dict
        return dict
    
    def validate_cell(self, value, type):
        ''' Ensures that the cells of each column conform to the column's type '''
        
        validator_factory = cell_validator_factory.MicrobeDirectoryCellValidatorFactory()
        
        if type == 'cogem_pathogenicity':
            validator = validator_factory.createCogemPathogenicityValidator()
        elif type == 'range':
            validator = validator_factory.createRangeValidator()
        elif type == 'binary':
            validator = validator_factory.createBinaryValidator()
        elif type == 'ternary':
            validator = validator_factory.createTernaryValidator()
        
        return validator.isValid(value)
    
    def export_as_sqlite(self, db_path):
        try:
            self.dict
        except:
            self.export_as_dictionary()
        
        # Delete the old db (if it exists) and remake it
        if os.path.isfile(db_path):
            os.remove(db_path)
            
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
            
        # Create tables
        tables_sql = {}
        
        tables_sql['Microbe'] = '''CREATE TABLE Microbe (
            'microbe_id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'kingdom' TEXT,
            'phylum' TEXT,
            'class' TEXT,
            'order' TEXT,
            'family' TEXT,
            'genus' TEXT,
            'species' TEXT NOT NULL,
            'optimal_pH' TEXT,
            'optimal_temperature' TEXT,
            'pathogenicity' INTEGER,
            'antimicrobial_susceptibility' INTEGER,
            'spore_forming' INTEGER,
            'biofilm_forming' INTEGER,
            'extreme_environment' INTEGER,
            'microbiome_location' INTEGER,
            'plant_pathogen' INTEGER,
            'animal_pathogen' INTEGER,
            'gram_stain' INTEGER
        );'''
        
        tables_sql['Antimicrobial'] = '''CREATE TABLE Antimicrobial (
            'antimicrobial_id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'name' TEXT NOT NULL
        );'''
        
        tables_sql['MicrobiomeLocation'] = '''CREATE TABLE MicrobiomeLocation (
            'microbiome_location_id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'name' TEXT NOT NULL
        );'''
        
        tables_sql['ExtremeEnvironment'] = '''CREATE TABLE ExtremeEnvironment (
            'sample_id' INTEGER PRIMARY KEY,
            'name' TEXT NOT NULL
        );'''
        
        tables_sql['Citation'] = '''CREATE TABLE Citation (
            'citation_id' INTEGER PRIMARY KEY,
            'microbe_id' INTEGER NOT NULL,
            'microbe_key' TEXT NOT NULL,
            'key_indices' TEXT NOT NULL DEFAULT '0',
            'citation' TEXT NOT NULL,
            'access_date_timestamp' INTEGER NOT NULL,
            FOREIGN KEY('microbe_id') REFERENCES Microbe('microbe_id')
        );'''
        
        for table in tables_sql:
            cursor.execute(tables_sql[table])
        
        # -------------
        # Add the python data to the db
        # -------------
        
        def add_quotes(list):
            new_list = []
            for item in list:
                item = "'{}'".format(item)
                new_list.append(item)
            return new_list
        
        for species in self.dict:
            keys = self.dict[species].keys()
            values = self.dict[species].values()
            
            if(len(values) == 0):
                continue
            
            keys = add_quotes(keys)
            values = add_quotes(values)
            
            keys = ','.join(keys)
            values = ','.join(values)
            
            cursor.execute("INSERT INTO 'Microbe' ({}) VALUES ({})".format(keys, values))
        
        connection.commit()
        connection.close()
        
    def __split_taxonomy_string(self, taxa):
        ''' Splits input text from col 1 of spreadsheet into taxa '''
        expr = re.compile('[a-z]__([A-Za-z]+)')
        while expr.match(taxa):
            taxa = re.sub(expr, '\\1', taxa)
        taxa = taxa.replace('_', ' ')
        taxa = taxa.split('|')
        return taxa