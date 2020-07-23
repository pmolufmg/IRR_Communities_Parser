#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module is preprocess text strings
"""
from . import patterns
import re

def replace_pattern(string, pattern, new=''):
    return pattern.sub(new, string)

def remove_extra_spaces(string):
    mono_spaced = string.strip(' ')
    mono_spaced = replace_pattern(mono_spaced, patterns.extra_spaces, ' ')
    
    return mono_spaced

def remove_noise(string, remove_words=False):
    clean_string = replace_pattern(string, patterns.char_noise)
    
    if remove_words:
        clean_string = replace_pattern(clean_string, patterns.description_noise)
        
    clean_string = remove_extra_spaces(clean_string)
    
    return clean_string

def remove_remarks_and_special_chars(string):
    reduced_string = replace_pattern(string, patterns.remarks, ' ')
    reduced_string = replace_pattern(reduced_string, patterns.special_chars_noise, ' ')
    reduced_string = remove_extra_spaces(reduced_string)
    
    return reduced_string

def clean_prepend_description(string, asn):
    descr = replace_pattern(string, eval(patterns.asn_noise))
    descr = replace_pattern(descr, patterns.prepend_times_noise)
    descr = remove_extra_spaces(descr)
    
    return descr

def remove_asn_from_line(asn, string):
    try:
        asn_pattern = eval(patterns.self_asn)
        new_string = replace_pattern(string, asn_pattern, ' ')
        new_string = remove_extra_spaces(new_string)
        return new_string
    
    except (ValueError, AttributeError):
        return string
    
def remove_negation_types(asn, string, _type=''):
    asn_free = remove_asn_from_line(asn, string)
    positive_string  = replace_pattern(asn_free, patterns.negation, ' ')
    
    if not _type:
        return positive_string
    
    try:
        type_pattern = eval(f"patterns.{_type}")
        new_string = replace_pattern(positive_string, type_pattern, ' ')
        new_string = remove_extra_spaces(new_string)
        
        return new_string
    
    except(NameError, ValueError):
        return positive_string
    