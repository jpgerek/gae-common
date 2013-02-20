# coding: utf-8
import os
import sys

STATICS_VERSIONING = 20 # If this one changes page caching has to changed else the url stays cached.
PAGE_CACHING_MASTER_VERSION = "%s:%s" % (STATICS_VERSIONING, 27) # Increase it when some html from a cached paged has changed before pushing code to life.
PRODUCT_NAME = ''
DOMAIN = ''
WEB_DOMAIN = 'www.%s' % DOMAIN
EMAIL_SENDER_NAME = u'%s \u30b7' % PRODUCT_NAME # \u30b7 -> utf-8 smiley.
EMAIL_SENDER = "@%s" % DOMAIN
EMAIL_SENDER_FULL = '%s <%s>' % (EMAIL_SENDER_NAME, EMAIL_SENDER)
EMAIL_SUBJECT_PREFIX = ''
SESSION_SECRET_KEY = ''
DEVELOPMENT = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
GOOGLE_ANALYTICS_ID = ''
BITLY_USERNAME = ''
BITLY_APIKEY = ''
SENGRID_USERNAME = ''
SENGRID_API_KEY = '*'