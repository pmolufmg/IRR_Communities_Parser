#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to find "NO-ADVERTISE" Communities information
"""

from _types.type_parser import CommunityTypes

class NoAdvertise(CommunityTypes):
    def __init__(self, type_name='NO_ADVERTISE'):
        super().__init__(type_name, negation=True)