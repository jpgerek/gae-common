# coding: utf-8
import re
from HTMLParser import HTMLParser

def strip_tags(html):
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

def nlbr(text):
    return re.sub(r'(\n)|(\r\n)', '<br/>', text)

def int_or_zero(int_val):
    try:
        int_val = int(int_val)
    except ValueError:
        int_val = 0
    except TypeError:
        int_val = 0
    return int_val

def param_from_list(input, valid_values):
    return input if valid_values[input] else ''

def validate_list(list, valid_items):
    for i in list:
        if i not in valid_items:
            return False
    return True

def htmlentitydecode(s):
    import htmlentitydefs

    # First convert alpha entities (such as &eacute;)
    # (Inspired from http://mail.python.org/pipermail/python-list/2007-June/443813.html)
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" " # Unknown entity: We replace with a space.

    t = re.sub(u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)
    # Then convert numerical entities (such as &#233;)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)
    # Then convert hexa entities (such as &#x00E9;)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1),16)), t)