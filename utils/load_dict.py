#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to load an existing communities json or 
to create a new one.
""" 

from . import defaults
from os import path
from collections import defaultdict
from ast import literal_eval
from json import loads

class LoadCommunitiesDict:
    
    def __init__(self, output_path):

        self.file_path = output_path
        
    def get_data_structure(self):
        
        if path.isfile(self.file_path):
            
            try:
                data = open(self.file_path).read()
                data_dict = literal_eval(loads(data))
                
                if not data_set:
                    raise ValueError
                
                print(f"Data set loaded from {self.file_path}:\n\
                    {len(data_set.keys())} ASN found in Data set.\n")
                
                return defaultdict(str, data_dict)
            
            except (ValueError, SyntaxError):
                pass
            
        else:
            open(self.file_path, 'w').close()
            
            print(f"New dataset created at {self.file_path}.\n")
            
        return defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

            