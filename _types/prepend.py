#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to find "PREPEND" Communities information
"""

from .commons import patterns
from .commons import preprocess
from .commons import fetch_values
import re

class Prepend:
    def __init__(self, type_name='PREPEND', max_prepend_number=11):
        '''
        keywords:
            type_name: name used do identify prepend communities in output
                    (must be "prepend" but the letter case may vary).
            
            max_prepend_number: Defines the range of prepend numbers to search for communities.
                    (from 1 to 11 (inclusive))
        '''
        
        self.assert_prepend_name(type_name)
        self.assert_prepend_number(max_prepend_number)
        
        '''Prepend types: "Prepend 1x", ..., "Prepend 11x"'''
        
        self.prepend_types = [f"{type_name} {str(num)}x" for num in range(1, max_prepend_number+1)]

    def parse(self, asn, line):
        community, new_line = fetch_values.get_community_value(line)
            
        if not community:
            return None, None, None
        
        new_line = preprocess.replace_pattern(new_line, patterns.prepend, ' ')
        _type, new_line = self.get_prepend_number(asn, new_line)
        
        description_line = preprocess.clean_prepend_description(new_line, asn)
        description = fetch_values.get_community_description(asn, description_line, treshold=5)
            
        return community, _type, description

    '''
    Find out the prepend number based on possible synonyms
    (e.g. "one time" == "once" == "1x").
    '''

    def get_prepend_number(self, asn, line):
        for _type in patterns.prepend_synonyms:
            pattern = patterns.prepend_synonyms[_type]
            synonym_pattern = re.compile(pattern, re.IGNORECASE)
            
            if synonym_pattern.search(line):
                new_line = preprocess.replace_pattern(line, synonym_pattern)
                
                return _type, new_line

        return self.count_asn_occurrences(asn, line)

    '''
    Find out prepend number based on textual description
    (e.g. "Prepend AS1 AS1 AS1" == "Prepend 2x").
    '''
    
    def count_asn_occurrences(self, asn, line):
        asn_format = '{0}|AS{0}'.format(asn)
        asn_pattern = re.compile(asn_format, re.IGNORECASE)
        asn_list = asn_pattern.findall(line)
        prep_count = len(asn_list)
        
        if prep_count:
            new_line = preprocess.replace_pattern(line, asn_pattern)
            
            return self.prepend_key_index(prep_count),\
                    preprocess.remove_extra_spaces(new_line)

        else:
            return self.prepend_types[0], line
        
    '''
    The number of ASNS counted in the description of the community 
    corresponds to the number of prepends.
    '''
    def prepend_key_index(self, num):
        if 1 <= num <= len(self.prepend_types):
            return self.prepend_types[num - 1]

        else:
            return self.prepend_types[0]

    @staticmethod
    def assert_prepend_name(name):
        try:
            assert(name.lower() == 'prepend')
            
        except (AssertionError, TypeError):
            print('The name must be "prepend" (case insensitive string).')
            
            raise SystemExit
    
    @staticmethod        
    def assert_prepend_number(num):
        try:
            assert(0 < num <= 11)
        
        except (AssertionError, TypeError):
            print('Prepend number must be and integer between 1 and 11 (inclusive).')
            
            raise SystemExit