import abc
import re

class AbstractValidator:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractclassmethod
    def isValid(self, value):
        pass

class NotBlankValidator(AbstractValidator):
    def isValid(self, value):
        return (value != None) and (value.strip() != '')
    
class NotNAValidator(AbstractValidator):
    __NA_TERMS = ['#n/a', 'n/a', 'na', 'none']
    
    def isValid(self, value):
        return value.lower() not in NotNAValidator.__NA_TERMS

class IntegerWithinRangeValidator(AbstractValidator):
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def isValid(self, value):
        pattern = re.compile('^[{min}-{max}]$'.format(min=self.min, max=self.max))
        return bool(pattern.match(value))

class RangeValidator(AbstractValidator):
    def isValid(self, value):
        pattern = re.compile('^((-?[0-9]+\.?[0-9]*)([:](-?[0-9]+\.?[0-9]*))?)(,((-?[0-9]+\.?[0-9]*)([:](-?[0-9]+\.?[0-9]*))?))*$')
        return bool(pattern.match(value.lower()))

class CompositeValidator(AbstractValidator):
    def __init__(self):
        self.__validators = []
    
    def add_validator(self, validator):
        self.__validators.append(validator)
    
    def isValid(self, value):
        for validator in self.__validators:
            if not validator.isValid(value):
                return False
        return True
        