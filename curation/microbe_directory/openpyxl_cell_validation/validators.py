# -*- coding: utf-8 -*-

import abc
import re
import regex
import numpy as np

class AbstractValidator:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractclassmethod
    def validate(self, value):
        pass

class NotBlankValidator(AbstractValidator):
    def validate(self, value):
        stripped = value.strip()
        return (value != None) and (stripped != '') and stripped
    
class NotNAValidator(AbstractValidator):
    __NA_TERMS = ['#n/a', 'n/a', 'na', 'none']
    
    def validate(self, value):
        stripped = value.strip()
        return (stripped.lower() not in NotNAValidator.__NA_TERMS) and stripped

class IntegerWithinRangeValidator(AbstractValidator):
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def validate(self, value):
        pattern = re.compile('^([{min}-{max}])$'.format(min=self.min, max=self.max))
        result = pattern.match(value.strip())
        return bool(result) and result.group(1)

class RangeValidator(AbstractValidator):
    '''Turns a range into an average of all the ranges'''
    def validate(self, value):
        range_chars = ':', '\-', '–'
        float_regex = '(?P<float>-?[0-9]+\.?[0-9]*)'
        single_range_regex = '(?P<range>\s*{float}\s*(\s*[{range_chars}]\s*{float}\s*)?)'.format(float=float_regex, range_chars=''.join(range_chars))
        multiple_range_regex = '^{single_regex}\s*(\s*,\s*{single_regex}\s*)*$'.format(single_regex=single_range_regex)
        
        result = regex.search(multiple_range_regex, value)
        if not result:  return False
        
        ranges = result.captures('range')
        
        range_averages_1 = [] # avg of each individual range
        for range in ranges:
            result = regex.search(single_range_regex, range)
            floats = result.captures('float')
            range_averages_1.append(np.mean(list(map(float, floats))))
        
        range_averages_2 = np.mean(range_averages_1) # avg of the avg of ranges
        return range_averages_2

class CompositeValidator(AbstractValidator):
    def __init__(self):
        self.__validators = []
    
    def add_validator(self, validator):
        self.__validators.append(validator)
    
    def validate(self, value):
        for validator in self.__validators:
            value = validator.validate(value)
            
            if not value:
                return False
        return value