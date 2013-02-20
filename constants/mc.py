# coding: utf-8
#NEVER USE % AS A LITERAL IN THE KEY NAME !!!
#IT WOULD CRASH THE CACHEIT DECORATOR

from config import PAGE_CACHING_MASTER_VERSION

""" Each time the page content changes these keys have to be changed or invalidated """
URL_KEY = 'URL:' + str(PAGE_CACHING_MASTER_VERSION) + ':5:%s'
ETAG_KEY = 'URL_ETAG:' + str(PAGE_CACHING_MASTER_VERSION) + ':5:%s'
REQUEST_HIT_FROM_IP = 'REQUEST_HIT_FROM_IP:%d:%s:%s:0' # Minute, url, ip.
IP_BAN = 'IP_BAN:%s:0' # IP
EMAIL_COUNTER = 'EMAIL_COUNTER:0' # Count