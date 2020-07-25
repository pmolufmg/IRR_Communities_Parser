#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to find "BLACKHOLE" Communities information
"""

from _types.type_parser import CommunityTypes

class BlackHole(CommunityTypes):
    
    def __init__(self, type_name='BLACKHOLE'):
        super().__init__(type_name)
        
        

