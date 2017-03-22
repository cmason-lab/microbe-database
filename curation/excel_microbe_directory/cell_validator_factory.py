from openpyxl_cell_validation import validators

class MicrobeDirectoryCellValidatorFactory():
    def createCogemPathogenicityValidator(self):
        validator = validators.CompositeValidator()
        validator.add_validator(validators.NotBlankValidator())
        validator.add_validator(validators.NotNAValidator())
        validator.add_validator(validators.IntegerWithinRangeValidator(1, 4))
        return validator
    
    def createRangeValidator(self):
        validator = validators.CompositeValidator()
        validator.add_validator(validators.NotBlankValidator())
        validator.add_validator(validators.NotNAValidator())
        validator.add_validator(validators.RangeValidator())
        return validator
    
    def createBinaryValidator(self):
        validator = validators.CompositeValidator()
        validator.add_validator(validators.NotBlankValidator())
        validator.add_validator(validators.NotNAValidator())
        validator.add_validator(validators.IntegerWithinRangeValidator(0, 1))
        return validator
    
    def createTernaryValidator(self):
        validator = validators.CompositeValidator()
        validator.add_validator(validators.NotBlankValidator())
        validator.add_validator(validators.NotNAValidator())
        validator.add_validator(validators.IntegerWithinRangeValidator(0, 2))
        return validator