from . import validators

class MicrobeDirectoryCellValidatorFactory():
    def __createDefaultValidator(self):
        validator = validators.CompositeValidator()
        validator.add_validator(validators.NotBlankValidator())
        validator.add_validator(validators.NotNAValidator())
        return validator
    
    def createCogemPathogenicityValidator(self):
        validator = self.__createDefaultValidator()
        validator.add_validator(validators.IntegerWithinRangeValidator(1, 4))
        return validator
    
    def createRangeValidator(self):
        validator = self.__createDefaultValidator()
        validator.add_validator(validators.RangeValidator())
        return validator
    
    def createBinaryValidator(self):
        validator = self.__createDefaultValidator()
        validator.add_validator(validators.IntegerWithinRangeValidator(0, 1))
        return validator
    
    def createTernaryValidator(self):
        validator = self.__createDefaultValidator()
        validator.add_validator(validators.IntegerWithinRangeValidator(0, 2))
        return validator