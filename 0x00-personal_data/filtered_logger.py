#!/usr/bin/env python3
"""Regex-ing"""

import re


def filter_datum(fields, redaction, message, separator):
    """function filter_datum"""
    newmessage = message
    for field in fields:
        newmessage = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', newmessage)
    return newmessage
