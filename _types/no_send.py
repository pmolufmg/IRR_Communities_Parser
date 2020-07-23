#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to find undefined "NO-SEND" Communities information
"""

from .commons import preprocess
from .commons import fetch_values

class NoSend:
    def __init__(self, type_name='NO_SEND'):
            
        '''
        keywords:
            type_name: name used do identify no_send communities in output

        '''
        
        self.type_name = type_name
        
    def parse(self, asn, line):
        community, new_line = fetch_values.get_community_value(line)
            
        if not community:
            return None, None, None
        
        new_line = preprocess.remove_negation_types(asn, new_line, _type='send')
        description = fetch_values.get_community_description(asn, new_line)

        return community, self.type_name, description