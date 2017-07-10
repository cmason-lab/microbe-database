import sqlite3

from .config import Columns

class MicrobeDirectory():
    def __init__(self, sqlite_path):
        self.connection = sqlite3.connect(sqlite_path)
        self.cursor = self.connection.cursor()
    
    def get_optimal_ph_column(self):
        return self.__get_column(Columns.OPTIMAL_PH)    
    def get_optimal_temperature_column(self):
        return self.__get_column(Columns.OPTIMAL_TEMPERATURE)
    def get_pathogenicity_column(self):
        return self.__get_column(Columns.PATHOGENICITY)   
    def get_antimicrobial_susceptibility_column(self):
        return self.__get_column(Columns.ANTIMICROBIAL_SUSCEPTIBILITY)
    def get_spore_forming_column(self):
        return self.__get_column(Columns.SPORE_FORMING)
    def get_biofilm_forming_column(self):
        return self.__get_column(Columns.BIOFILM_FORMING)
    def get_gram_stain_column(self):
        return self.__get_column(Columns.GRAM_STAIN) 
    def get_microbiome_location_column(self):
        return self.__get_column(Columns.MICROBIOME_LOCATION)   
    def get_plant_pathogen_column(self):
        return self.__get_column(Columns.PLANT_PATHOGEN)
    def get_animal_pathogen_column(self):
        return self.__get_column(Columns.ANIMAL_PATHOGEN)
    
    def __get_column(self, column_name):
        query = "SELECT species, {column_name} FROM Microbe WHERE {column_name} IS NOT NULL;".format(column_name=column_name.lower())
        self.cursor.execute(query)
        return {species: column_value for species, column_value in self.cursor.fetchall()}
    
    def get_microbe(self, species_name):
        '''Make this into its own class later instead of returning a dict'''
        query = "SELECT * FROM Microbe WHERE species='{species_name}';".format(species_name=species_name)
        self.cursor.execute(query)
        col_values = self.cursor.fetchone() # returns as a tuple
        col_names = [x[0] for x in self.cursor.description]
        return {col_name: col_value for col_name, col_value in zip(col_names, col_values)} # access as result[col_name]
        
#class Microbe():