#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to convert command line arguments into file paths.
""" 

from . import defaults
from re import match
import argparse
import os

class GetArgs:
    
    def __init__(self):
        
        self.cmd_line_parser = argparse.ArgumentParser(prog='pyhon parse.py',
                                                       formatter_class=argparse.RawDescriptionHelpFormatter,
                                                       description='''\
IRR Communities Parser
----------------------

1. Reads all "$ASN$.txt" files in --input dir
2. Collects BGP Communities information from files contents
3. Stores collected info as "communities.json" in --output dir
''',
                                                        epilog='''\
IMPORTANT: Input files must be in the standard IRR response format (RPSL)
and must be named according to their respective ASN (ASN.txt).''')
        
        self.add_arguments()
        self.args = self.cmd_line_parser.parse_args()
        self.verify_args()

    def add_arguments(self):
        self.cmd_line_parser.add_argument('-i', '--input',
                                        default = defaults.irr_dir_path,
                                        dest='irr_dir',
                                        metavar='input_dir',
                                        type = str,
                                        help="root dir where the IRR files are stored")

        self.cmd_line_parser.add_argument('-o', '--output',
                                        default=defaults.json_output_dir_path,
                                        dest='json_dir',
                                        metavar='output_dir',
                                        type = str,
                                        help="dir where communities.json file will be stored.")

    def verify_args(self):
        if not os.path.isdir(self.args.irr_dir):
            print(f"Invalid input dir ({self.args.irr_dir})")
            
        elif not os.path.isdir(self.args.json_dir):
            print(f"Invalid output dir ({self.args.json_dir})")
            
        else:
            if not self.args.irr_dir.endswith('/'):
                self.args.irr_dir += '/'
            
            if not self.args.json_dir.endswith('/'):
                self.args.json_dir += '/'
                
            return
        
        self.cmd_line_parser.print_help()
        
        raise SystemExit
        
    def get_system_paths(self):
        irr_file_list = self.get_irr_file_list()
        out_json, out_csv = self.get_output_files()
        
        return \
            irr_file_list,\
            out_json,\
            out_csv
        
    def get_irr_file_list(self):
        irr_list = []
        
        for dirname, _, filenames in os.walk(self.args.irr_dir):
            for filename in filenames:
                
                if match('\d+', filename) and filename.endswith('.txt'):
                    file_path = os.path.join(dirname, filename)
                    irr_list.append(file_path)
        
        if not irr_list:
            print(f"No txt files in {self.args.irr_dir}")
            
            raise SystemExit
        
        return irr_list
    
        
    def get_output_files(self):
        json_file = self.args.json_dir + defaults.output_filename
        csv_file = self.args.json_dir + defaults.communities_table
        
        return json_file, csv_file