# coding: utf-8
import logging
import config

from google.appengine.api import memcache

import helpers

ACTIVE = not config.DEVELOPMENT

DEFAULT_CACHING_TIME = 0 #0 means non expiring time

mc = memcache.Client()

@helpers.retry()
def get(key, for_cas=False):
    return None if ACTIVE is False else mc.get(key, for_cas=for_cas)

@helpers.retry()
def set(key, dataset, time=DEFAULT_CACHING_TIME):
    return None if ACTIVE is False else mc.set(key, dataset, time)

@helpers.retry()
def cas(key, dataset, time=DEFAULT_CACHING_TIME):
    return None if ACTIVE is False else mc.cas(key, dataset, time=time)

@helpers.retry()
def add(key, dataset, time=DEFAULT_CACHING_TIME):
    return None if ACTIVE is False else mc.add(key, dataset, time=time)

@helpers.retry()
def incr(key, initial_value=0, time=DEFAULT_CACHING_TIME, delta=1):
    return None if ACTIVE is False else mc.incr(key, initial_value=initial_value, delta=delta)

@helpers.retry()
def delete(key):
    return mc.delete(key)

#keyformat admits % placeholders
def cacheit(keyformat, time=DEFAULT_CACHING_TIME, add_instead_of_set=False):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            key = keyformat % args[:keyformat.count('%')]
            data = get(key)
            if data is None:
                data = fxn(*args, **kwargs)
                if add_instead_of_set:
                    add(key, data, time)
                else:
                    set(key, data, time)
            return data
        return wrapper
    return decorator