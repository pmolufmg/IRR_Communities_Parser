#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is preprocess text strings
"""
from _types.commons.patterns import RegExPatterns
import re
class Preprocess:
    def __init__(self):
        self.patterns = RegExPatterns()
        
    def replace_pattern(self, string, pattern, new=''):
        return pattern.sub(new, string)

    def remove_extra_spaces(self, string):
        mono_spaced = string.strip(' ')
        mono_spaced = self.replace_pattern(mono_spaced, self.patterns.extra_spaces, ' ')
        
        return mono_spaced

    def remove_noise(self, string, remove_words=False):
        clean_string = self.replace_pattern(string, self.patterns.char_noise)
        
        if remove_words:
            clean_string = self.replace_pattern(clean_string, self.patterns.description_noise)
            
        clean_string = self.remove_extra_spaces(clean_string)
        
        return clean_string

    def remove_remarks_and_special_chars(self, string):
        reduced_string = self.replace_pattern(string, self.patterns.remarks, ' ')
        reduced_string = self.replace_pattern(reduced_string, self.patterns.special_chars_noise, ' ')
        reduced_string = self.remove_extra_spaces(reduced_string)
        
        return reduced_string


    def clean_prepend_description(self, string, asn):
        descr = self.replace_pattern(string, eval(self.patterns.asn_noise))
        descr = self.replace_pattern(descr, self.patterns.prepend_times_noise)
        descr = self.remove_extra_spaces(descr)
        
        return descr

    def remove_asn_from_line(self, asn, string):
        try:
            asn_pattern = eval(self.patterns.self_asn)
            new_string = self.replace_pattern(string, asn_pattern, ' ')
            new_string = self.remove_extra_spaces(new_string)
            return new_string
        
        except (ValueError, AttributeError):
            return string

    def remove_negation_types(self, asn, string, _type=''):
        asn_free = self.remove_asn_from_line(asn, string)
        positive_string  = self.replace_pattern(asn_free, self.patterns.negation, ' ')
        
        if not _type:
            return positive_string
        
        try:
            type_pattern = eval(f"self.patterns.{_type}")
            new_string = self.replace_pattern(positive_string, type_pattern, ' ')
            new_string = self.remove_extra_spaces(new_string)
            
            return new_string
        
        except(NameError, ValueError):
            return positive_string