# coding: utf-8
import re

# Took from django validator.
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)

def is_a_valid_email(email):
    return email_re.match(email) is not None

def validate_list( list, valid_items ):
    for i in list:
        if i not in valid_items:
            return False
    return True

custom_base64_regex = r'[a-zA-Z0-9_\.\+-]+' # It uses . instead of = for padding
base64_regex = r'[a-zA-Z0-9_=\+-]+'

compiled_custom_base64_regex = re.compile(custom_base64_regex)
def is_valid_custom_base64(text):
    return compiled_custom_base64_regex.match(text) is not None

compiled_base64_regex = re.compile(base64_regex)
def is_valid_base64(text):
    return compiled_base64_regex.match(text) is not None

int_regex = r'^\d+$'
compiled_int_regex = re.compile(int_regex)
def is_int(text):
    return compiled_int_regex.match(text) is not None

hex_regex = r'^[\dA-F]+$'
compiled_hex_regex = re.compile(hex_regex)
def is_hex(text):
    return compiled_hex_regex.match(text) is not None
