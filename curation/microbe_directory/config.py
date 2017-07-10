class Columns():
    OPTIMAL_PH = 'OPTIMAL_PH'
    OPTIMAL_TEMPERATURE = 'OPTIMAL_TEMPERATURE'
    PATHOGENICITY = 'PATHOGENICITY'
    ANTIMICROBIAL_SUSCEPTIBILITY = 'ANTIMICROBIAL_SUSCEPTIBILITY'
    SPORE_FORMING = 'SPORE_FORMING'
    BIOFILM_FORMING = 'BIOFILM_FORMING'
    EXTREME_ENVIRONMENT = 'EXTREME_ENVIRONMENT'
    GRAM_STAIN = 'GRAM_STAIN'
    MICROBIOME_LOCATION = 'MICROBIOME_LOCATION'
    PLANT_PATHOGEN = 'PLANT_PATHOGEN'
    ANIMAL_PATHOGEN = 'ANIMAL_PATHOGEN'

class Taxa():
    KINGDOM = 'KINGDOM'
    PHYLUM = 'PHYLUM'
    CLASS = 'CLASS'
    ORDER = 'ORDER'
    FAMILY = 'FAMILY'
    GENUS = 'GENUS'
    SPECIES = 'SPECIES'    
    
class ColumnValidationTypes():
    '''Custom types corresponding to what's acceptable to be in a given spreadsheet cell'''
    BINARY = 'BINARY'
    TERNARY = 'TERNARY'
    RANGE = 'RANGE' # these will be converted to an average
    COGEM_PATHOGENICITY = 'COGEM_PATHOGENICITY'

class SqlDataTypes():
    TEXT = 'TEXT'
    INTEGER = 'INTEGER'
    REAL = 'REAL' # float

class SpreadsheetConfig():
    class __SpreadsheetConfig():
        def __init__(self):
            self._COLUMNS = {
                Columns.OPTIMAL_PH: {
                    'column': 13,
                    'validation_type': ColumnValidationTypes.RANGE,
                    'sql_data_type': SqlDataTypes.REAL
                },
                Columns.OPTIMAL_TEMPERATURE: {
                    'column': 15,
                    'validation_type': ColumnValidationTypes.RANGE,
                    'sql_data_type': SqlDataTypes.REAL
                },
                Columns.PATHOGENICITY: {
                    'column': 19,
                    'validation_type': ColumnValidationTypes.COGEM_PATHOGENICITY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.ANTIMICROBIAL_SUSCEPTIBILITY: {
                    'column': 29,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.SPORE_FORMING: {
                    'column': 49,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.BIOFILM_FORMING: {
                    'column': 51,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.EXTREME_ENVIRONMENT: {
                    'column': 3,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.GRAM_STAIN: {
                    'column': 41,
                    'validation_type': ColumnValidationTypes.TERNARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.MICROBIOME_LOCATION: {
                    'column': 7,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.PLANT_PATHOGEN: {
                    'column': 33,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                },
                Columns.ANIMAL_PATHOGEN: {
                    'column': 35,
                    'validation_type': ColumnValidationTypes.BINARY,
                    'sql_data_type': SqlDataTypes.INTEGER
                }
            }
        
        def getColumnNames(self):
            return list(self._COLUMNS.keys())
        
        def getColumnNumber(self, column_name):
            return self._COLUMNS[column_name]['column']
        
        def getColumnValidationType(self, column_name):
            return self._COLUMNS[column_name]['validation_type']
        
        def getSqlDataType(self, column_name):
            return self._COLUMNS[column_name]['sql_data_type']
        
        def getTaxaHierarchy(self):
            return [Taxa.KINGDOM, Taxa.PHYLUM, Taxa.CLASS, Taxa.ORDER, Taxa.FAMILY, Taxa.GENUS, Taxa.SPECIES]
        
    instance = None
    def __init__(self):
        if not SpreadsheetConfig.instance:
            SpreadsheetConfig.instance = SpreadsheetConfig.__SpreadsheetConfig()
    def __getattr__(self, attr_name):
        return getattr(SpreadsheetConfig.instance, attr_name)