#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to generate the output files and summarize the results
""" 

from collections import defaultdict
from collections import Counter
from os.path import isfile
from json import dump
import pandas as pd

class Output:
    
    def __init__(self, data_dict, json_file, csv_file):
        
        self.data_dict = data_dict
        self.json_file = json_file
        self.csv_file = csv_file
        
        self.summary = defaultdict(lambda: Counter())
        self.summary_keys = ['ASNs', 'COMMUNITIES']
        
        self.asn_set = set()
        self.prepend_accumulator = 'TOTAL PREPENDS'
        
    def save_files_and_summarize_results(self):
        self.save_json()
        self.save_csv()
        self.summarize_to_stdout()
        
    def save_json(self):
        with open(self.json_file, 'w') as json_file:
            dump(self.data_dict, json_file, sort_keys=True)
    
    def save_csv(self):
        self.write_csv_header()
        self.write_csv_body()
        
    def write_csv_header(self):
        header = 'asn,type,community,description\n'
        open(self.csv_file, 'w').write(header)
                
    def write_csv_body(self):
        csv_body = ''
        
        for asn in self.data_dict:
            for _type in self.data_dict[asn]:
                self.count_elements(asn, _type, key=0)
                
                for community in self.data_dict[asn][_type]:
                    self.count_elements(asn, _type, key=1)
                    
                    description = self.data_dict[asn][_type][community]
                    
                    csv_body += f"{asn},{_type},{community},{description}\n"
        
        open(self.csv_file, 'a').write(csv_body)
    
    def count_elements(self, asn, _type, key):
        element = self.summary_keys[key]
        self.summary[_type][element] += 1
        
        if _type.endswith('x'):
            if key or not asn in self.asn_set:
                self.summary[self.prepend_accumulator][element] += 1
                if not key:
                    self.asn_set.add(asn)
        
        
    def summarize_to_stdout(self):
        ordered_types = sorted(self.summary.keys(), key=self.sort_params)
        df = pd.DataFrame(self.summary)
        df = df.T
        df = df.reindex(index = ordered_types)
        print(df)

    @staticmethod
    def sort_params(str):
        return str[0], str[-2], len(str)