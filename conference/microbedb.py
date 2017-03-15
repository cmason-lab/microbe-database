import sqlite3

class MicrobeDB:
    def __init__(self, db_path):
        self.keys_to_cols = {'optimal_pH': 13, 'optimal_temperature': 15, 'pathogenicity': 19,
            'antimicrobial_susceptibility': 29, 'spore_forming': 49, 'biofilm_forming': 51,
            'extreme_environment': 3, 'gram_stain': 41, 'microbiome_location': 7, 'plant_pathogen': 33,
            'animal_pathogen': 35}

        self.type_from_key = {'optimal_pH': 'range', 'optimal_temperature': 'range', 'pathogenicity': '1-4',
            'antimicrobial_susceptibility': 'binary', 'spore_forming': 'binary',
            'biofilm_forming': 'binary', 'extreme_environment': 'binary', 'gram_stain': '0-2',
            'microbiome_location': 'binary', 'plant_pathogen': 'binary', 'animal_pathogen': 'binary'}
        
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
    def binary_counts(self, species_query):
        binary_results = {}
        for key in self.type_from_key:
            type = self.type_from_key[key]
    
            if type == 'binary':
                query = "SELECT count({}) FROM Microbe WHERE {}=1 AND ({});".format(key, key, species_query)
                print('hi')
                print(species_query)
                print(query)
                print(' ')
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                
                if result:
                    count = result[0]
                else:
                    count = 0
                binary_results[key] = count
        return binary_results
    
    def pathogenicity_counts(self, species_query):
        pathogenicity_results = {}
        for i in range(1,4):
            query = "SELECT count({}) FROM Microbe WHERE pathogenicity={} AND ({});".format('pathogenicity', i, species_query)
            self.cursor.execute(query)
            result = self.cursor.fetchone()[0]
            pathogenicity_results[i] = result
        return pathogenicity_results
    
    def gram_stain_counts(self, species_query):
        gram_stain_results = {}
        for i in range(0,3):
            query = "SELECT count({}) FROM Microbe WHERE gram_stain={} AND ({});".format('gram_stain', i, species_query)
            self.cursor.execute(query)
            result = self.cursor.fetchone()[0]
            gram_stain_results[i] = result
        return gram_stain_results
    
    def optimal_pH_data(self, species_query):
        query = "SELECT species, optimal_pH FROM Microbe WHERE ({});".format(species_query)
        self.cursor.execute(query)
        optimal_pHs = self.cursor.fetchall()
        return optimal_pHs
    
    def optimal_temp_data(self, species_query):
        query = "SELECT species, optimal_temperature FROM Microbe WHERE ({});".format(species_query)
        self.cursor.execute(query)
        optimal_temps = self.cursor.fetchall()
        return optimal_temps