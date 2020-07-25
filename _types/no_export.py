#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is used to find "NO-EXPORT" Communities information
"""

from _types.type_parser import CommunityTypes

class NoExport(CommunityTypes):
    def __init__(self, type_name='NO_EXPORT'):
        super().__init__(type_name, negation=True)