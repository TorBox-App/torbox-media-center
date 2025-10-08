"""
Centralized regex patterns for media parsing.
All patterns are compiled at import time for optimal performance during repeated use.
"""

import re

# Regex to clean non-date characters from a string
DATE_CLEAN_PATTERN = re.compile(r'[^\d\-\./]')

# Regex to find a date anywhere in the filename
DATE_FIND_PATTERN = re.compile(r'(\d+\.\d+\.\d+|\d+\.\d+|\d+/\d+/\d+|\d+-\d+-\d+)')

# Regex to find sports separator: vs, vs., v, v., at, @, versus
SPORT_SEPARATOR_PATTERN = re.compile(r'\s+(vs\.?|v\.?|at|@|versus)\s+', re.IGNORECASE)
# Regex to normalize whitespace (multiple spaces → single space)
WHITESPACE_PATTERN = re.compile(r'\s+')

# Pre-compiled patterns for parsing specific date formats
DATE_FORMAT_PATTERNS = [
    # US formats
    (re.compile(r'^(\d{1,2})/(\d{1,2})/(\d{4})$'), 'MM/DD/YYYY'),
    (re.compile(r'^(\d{1,2})\.(\d{1,2})\.(\d{4})$'), 'MM.DD.YYYY'),
    (re.compile(r'^(\d{1,2})-(\d{1,2})-(\d{4})$'), 'MM-DD-YYYY'),

    # ISO formats
    (re.compile(r'^(\d{4})-(\d{1,2})-(\d{1,2})$'), 'YYYY-MM-DD'),
    (re.compile(r'^(\d{4})/(\d{1,2})/(\d{1,2})$'), 'YYYY/MM/DD'),
    (re.compile(r'^(\d{4})\.(\d{1,2})\.(\d{1,2})$'), 'YYYY.MM.DD'),

    # European formats
    (re.compile(r'^(\d{1,2})\.(\d{1,2})\.(\d{4})$'), 'DD.MM.YYYY'),
    (re.compile(r'^(\d{1,2})-(\d{1,2})-(\d{4})$'), 'DD-MM-YYYY'),
    (re.compile(r'^(\d{1,2})/(\d{1,2})/(\d{4})$'), 'DD/MM/YYYY'),

]