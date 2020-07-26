#-*- coding: utf-8 -*-

"""
IRR Communities Parser: extract communities information from irr files

This module contains RegEx patterns used by the IRR Communities Parser
"""

from collections import OrderedDict
import re

class RegExPatterns:
    def __init__(self):
        # Generic patterns
        self.asn = re.compile('(as\s?\d+|asn\s?\d+)', re.IGNORECASE)

        self.self_asn = 're.compile(f"(?:\A|\w+|\D){asn}(?:\D|\Z)",re.IGNORECASE)'

        self.community = re.compile('(?:\A|\s)(\d+:\d+)(?:\s|\Z)')

        self.invalid_community = re.compile('\d+:\d+(\[\w|\{\w|\*|\$|[a-zA-Z])')

        self.remarks = re.compile('remarks:', re.IGNORECASE)

        self.destination = re.compile('(\A|\s)(to|for|through|towards{0,1}|at)(?=\s)', re.IGNORECASE)

        self.description_noise = re.compile('(\A|\s)(set|apply|communit(y|ies))(?=\s|\Z)', re.IGNORECASE)

        # Substrings Patterns used to stardardize strings
        self.special_chars = ['"', 
                        "'", 
                        '\\', 
                        '|', 
                        '/', 
                        '(', 
                        ')', 
                        '[', 
                        ']', 
                        '{', 
                        '}', 
                        '<', 
                        '>', 
                        '+', 
                        '=', 
                        '*', 
                        '!', 
                        '#', 
                        '$', 
                        '-', 
                        '_',
                        ',',
                        ';',
                        '.']

        self.char_noise = re.compile('\sx\s', re.IGNORECASE)

        self.extra_spaces = re.compile(' +')

        self.special_chars_noise = re.compile('[' + re.escape(''.join(self.special_chars)) + ']')

        self.asn_noise = 're.compile(f"(?<=\A)*(?<=\s)*(AS|ASN|AS NUMBER)?(?:\s)*({asn})(?=\D|\Z)", re.IGNORECASE)'

        self.prepend_times_noise = re.compile(r'times{0,1}', re.IGNORECASE)


        # Auxiliary negation patterns used with NO-EXPORT, NO-ADVERTISE and NO-SEND naming patterns
        self.negation = re.compile('(?:\A|\s)((do(n\s?t|\snot)?)|(no(t|ne|one|body)?))(?:\s|\Z)', re.IGNORECASE)

        self.negated_type_words = ['export', 'advertise', 'send']

        self.negated_types = re.compile('|'.join(self.negated_type_words), re.IGNORECASE)

        # Community type naming patterns

        ## PREPEND
        self.prepend = re.compile('pre(\s)?pend(\s|s|ing|ed)?', re.IGNORECASE)

        ## BLACKHOLE
        self.blackhole = re.compile('black(\s)?hol(e(s|d)?|ing)(?=\s|\Z)', re.IGNORECASE)

        ## NO_EXPORT
        self.export = re.compile('export(?=\s|\Z)', re.IGNORECASE)

        ## NO_ADVERTISE
        self.advertise = re.compile('advertise(?=\s|\Z)', re.IGNORECASE)

        ## NO_SEND
        self.send = re.compile('(sen(d|t)|announce|route)(?=\s|\Z)', re.IGNORECASE)


        # Equivalent terms (synonyms)

        ## PREPEND
        pat_begin = '(?:\A|\s)(x|times?)?'
        pat_end = '(x|times?)?(?=\s|\Z)'
        self.prepend_synonyms = OrderedDict([('PREPEND 1x', f"{pat_begin}(1|on(e|ce)|singlet?){pat_end}"),
                                        ('PREPEND 2x', f"{pat_begin}(2|tw(o|ice|in)|doublet?){pat_end}"),
                                        ('PREPEND 3x', f"{pat_begin}(3|thr(ee|ice)|triplet?){pat_end}"),
                                        ('PREPEND 4x', f"{pat_begin}(4|four|quadruplet?){pat_end}"),
                                        ('PREPEND 5x', f"{pat_begin}(5|five|quintuplet?){pat_end}"),
                                        ('PREPEND 6x', f"{pat_begin}(6|six|(s|h)extuplet?){pat_end}"),
                                        ('PREPEND 7x', f"{pat_begin}(7|seven|(s|h)eptuplet?){pat_end}"),
                                        ('PREPEND 8x', f"{pat_begin}(8|eight|octuplet?){pat_end}"),
                                        ('PREPEND 9x', f"{pat_begin}(9|nine|nonuplet?){pat_end}"),
                                        ('PREPEND 10x', f"{pat_begin}(10|ten|decuplet?){pat_end}"),
                                        ('PREPEND 11x', f"{pat_begin}(11|eleven|(un|hen)decuplet?){pat_end}")])