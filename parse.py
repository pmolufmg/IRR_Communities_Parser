#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files
""" 

from utils.sys_args import GetArgs
from utils.load_dict import LoadCommunitiesDict
from utils.output import Output
from _types.commons import preprocess
from _types.commons import patterns
from _types.prepend import Prepend
from _types.blackhole import BlackHole
from _types.no_export import NoExport
from _types.no_send import NoSend
from _types.no_advertise import NoAdvertise

class IrrCommunitiesParser:
    
    def __init__(self, irr_file_list, data_dict):
        
        self.irr_files = irr_file_list
        self.communities_dict = data_dict
        
        '''
        NO_SEND is an indefinite type of community (based on expressions such as "not send route", 
        "not announce", etc.) that can be interpreted as "NO_EXPORT" or "NO_ADVERTISE". 
        
         - "no_send_equivalent_type" is used to define the name by which the NO-SEND communities 
         will be registered in the output.
        '''
        no_send_equivalent_type = 'NO_EXPORT'
        
        '''
        Community type objects:
        - Responsible for the application of type-specific parsing methods.
         
        - The params for instantiation are optional.
            - type_name: string used as key to identify the community type in the output
            - max_prepend_number: define the range of prepend numbers to search
        
        - The order in which the types are to be fetched is defined by the "community_types" list.
            - The name in the list must be the same as the class variable that references the object.
        '''
        self.prepend = Prepend(type_name='PREPEND', max_prepend_number=11)
        self.blackhole = BlackHole(type_name='BLACKHOLE')
        self.no_export = NoExport(type_name='NO_EXPORT')
        self.no_advertise = NoAdvertise(type_name='NO_ADVERTISE')
        self.no_send = NoSend(type_name=no_send_equivalent_type)
        
        
        self.community_types = ['prepend', 'blackhole', 'no_export', 'no_advertise', 'no_send']
    
    def get_communities_from_irr_files(self):
        for _file in self.irr_files:
            
            with open(_file, encoding="ISO-8859-1") as rpsl_file:
                asn = _file.split('/')[-1].rstrip('.txt')
                lines = rpsl_file.read().splitlines()
                
                for line in lines:
                    line = preprocess.remove_extra_spaces(line)
                    
                    if not self.starts_with_community_or_remarks(line):
                        continue
                    
                    clean_line = preprocess.remove_remarks_and_special_chars(line)
                    
                    for community_type in self.community_types:
                        negation = community_type.startswith('no')

                        data = self.fetch_data(asn, clean_line, community_type, negation)
                        if data:
                            self.add_data_to_json(asn, data)
                            break
                        
        return self.communities_dict

    def add_data_to_json(self, asn, data):
        if len(data) != 3 or not data[0]:
            return
        
        community, _type, info = data        
        
        self.communities_dict[asn][_type][community] = info
                            
    def fetch_data(self, asn, line, _type, negation):
        if negation:
            if not patterns.negation.search(line):
                return False, False, False
            
            second_pattern = _type.lstrip('no_')
            type_pattern = eval(f"patterns.{second_pattern}")
        
        else:
            type_pattern = eval(f"patterns.{_type}")

        if type_pattern.search(line):
            type_parse= eval(f"self.{_type}.parse(asn, line)")
                
            return type_parse
    
    @staticmethod
    def starts_with_community_or_remarks(line):
        starts_with_remarks = patterns.remarks.match(line)
        starts_with_community = patterns.community.match(line)
        invalid_community_format = patterns.invalid_community.search(line)

        if (starts_with_remarks or starts_with_community)\
            and not invalid_community_format:    
            return True
        
        return False

 
if __name__ == "__main__":
    
    args = GetArgs()
    irr_file_list, json_file, csv_file = args.get_system_paths()
    
    output_template = LoadCommunitiesDict(json_file)
    communities_dict = output_template.get_data_structure()

    irr_parser = IrrCommunitiesParser(irr_file_list, communities_dict)
    collected_data = irr_parser.get_communities_from_irr_files()
    
    output = Output(collected_data, json_file, csv_file)
    output.save_files_and_summarize_results()
    