#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module contains generic methods to fetch, remove and retrieve community 
value and descriptive information from a given string.
"""

from _types.commons.preprocess import Preprocess
from _types.commons.patterns import RegExPatterns

class CommunityTypes:
    
    def __init__(self, type_name, negation=False):
        '''
        keywords:
            type_name: define type name in the output
        '''
        
        self.type_name = type_name
        self.negated_type = negation
        
        self.preprocess = Preprocess()
        self.patterns = RegExPatterns()
        
    def parse(self, asn, line):
        community, new_line = self.get_community_value(line)
            
        if not community:
            return None, None, None
        
        new_line = self.remove_type_from_line(asn, new_line)
        description = self.get_community_description(new_line)

        return community, self.type_name, description
    
    def remove_type_from_line(self, asn, string):
        if self.negated_type:
            try:
                _type = self.patterns.negated_types.search(self.type_name).group().lower()
                return self.preprocess.remove_negation_types(asn, string, _type=_type)
            except AttributeError:
                print(f"{self.type_name} is not a valid negated type.")
        
        return self.preprocess.remove_asn_from_line(asn, string)
            
            
    def get_community_value(self, line):
        try:
            '''Match with community pattern'''
            community = self.patterns.community.search(line).group()
            
            '''Remove Community and colon from line'''
            new_line = self.preprocess.replace_pattern(line, self.patterns.community)
            new_line = new_line.replace(':', '')
            
            return community.strip(' '), new_line

        except (ValueError, AttributeError):
            return None, line
            
    '''
    To find the destination for community application (get_info), 
    textual noises are removed and the "to/toward/for/through some AS/group" 
    pattern is searched for in the remaining text. 

    If the text does not present this type of description, 
    it is recorded as a general application community (registered as "to all").
    '''
    def  get_community_description(self, description, treshold=3):
        to_all = 'to all'

        if self.patterns.destination.search(description):
            description = self.patterns.destination.sub(' to ', description)
            description = description[description.index(' to') + 1:]
            as_list = self.patterns.asn.findall(description)
            
            if len(as_list) == 1:
                description = 'to ' + as_list[0]
            
            elif not description:
                description = to_all
        
        description = self.preprocess.remove_noise(description, remove_words=True)
        
        if len(description) < treshold:
            description = to_all
        
        return description.strip(' ')