# coding: utf-8
import os
import webapp2
import logging
import datetime
import statics_revisions
import helpers
import constants
from google.appengine.ext.webapp import template

import cachepy
import mc
import hashlib
import base64
import urllib
import json
import config
import time

class Base(webapp2.RequestHandler):
    URL = constants.url
    PAGE_CACHING_TIME_304 = 0 # Seconds, 0 means forever.
    IP_BAN_TIME = 120 # Seconds.

    def __init__(self, request, response):
        self.initialize(request, response)
        self._is_ajax = 'X-Requested-With' in self.request.headers and self.request.headers['X-Requested-With'] == 'XMLHttpRequest'

    def _get_content_etag(self, content):
        """ Generate an etag corresponding to a content """
        """
        It seems that some pages have unicode and other ascii.
        As temporal solution I just catch the exception.
        """
        try:
            content = content.encode('utf8')
        except UnicodeDecodeError:
            pass
        etag = base64.urlsafe_b64encode(hashlib.md5(content).digest()).rstrip("=")
        return '"%s"' % etag

    def set_cookie(self, name, value, path=None, days_of_life=0, minutes_of_life=0):
        import urllib
        value = urllib.quote(str(value))
        path = path or self.request.path
        if days_of_life == 0 and minutes_of_life is 0:
            cookie = "%s=%s; path=%s" %(name, value, path)
        else:
            timedelta = datetime.timedelta(days_of_life, minutes_of_life*60)
            expires = datetime.datetime.utcnow() + timedelta
            expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            cookie = "%s=%s; expires=%s; path=%s" % (name, value, expires_rfc822, path)
        self.response.headers.add_header("Set-Cookie", cookie)

    def delete_cookie(self, name):
        self.set_cookie(name, 'DELETED', -10)

    def is_ajax(self):
        return self._is_ajax

    def json_response(self, content_text, params={}):
        params['content_text'] = content_text
        self.set_http_content_type('application/json')
        self.response.write(json.dumps(params))

    def get_json_response(self, content_text, params={}):
        params['content_text'] = content_text
        return json.dumps(params)

    def http_no_caching(self):
        """
        Setting http caching policies
        """
        """ The caching is suggested for the end clients no the possible proxies in the middle"""
        self.response.headers['Cache-Control'] = 'private, max-age=0'
        #This one is just for http 1.0
        #self.response.headers['Pragma'] = 'no-cache'
        """ The vary headers makes IE browser to ommit the etags.
        Setting the Cache-Control to private wont create problems with the encoding without the Vary header.
        """
        self.response.headers['Vary'] = 'Accept-Encoding'
        """ Google uses expires -1 so it must be ok to mean the content is already expired """
        self.response.headers['Expires'] = '-1'

    def set_http_expires(self, days):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days)
        self.response.headers['Cache-Control'] = 'public'
        self.response.headers['Expires'] = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")

    def set_http_content_type(self, type, charset='utf-8'):
        self.response.headers['Content-Type'] = '%s; charset=%s' % (type, charset)

    def get_template_path(self, template_file):
        return os.path.join(os.path.dirname(__file__), '../templates/%s' % template_file)

    def get_template(self, template_file, params={}):
        params['revisions'] = statics_revisions.list
        params['config'] = config
        params['statics_domain'] = '' if config.DEVELOPMENT else "//statics.%s" % config.DOMAIN
        return template.render(self.get_template_path(template_file), params)

    def display_template(self, template_file, params={}):
        self.response.out.write(self.get_template(template_file, params))



    def display_page_or_304(self, get_page, expiry=PAGE_CACHING_TIME_304, request_path=None):
        """ It just uses etag because last-modified is for http 1.0 and nowadays no browser uses it """
        import mc
        content = None
        #- It's possible to customize the request path in case different requeste paths have the same content -#
        request_path = request_path or self.request.path
        #- Trying to get the etag from cachepy -#
        current_etag = cachepy.get(constants.cachepy.ETAG_KEY % request_path)
        #- There is no etag stored in cachepy.
        if current_etag is None:
            #- Trying to get the etag from mc.
            current_etag = mc.get(constants.mc.ETAG_KEY % request_path)
            if current_etag is None:
                #- MC doesn't have the etag either -#
                content = get_page() # Getting the page content.
                current_etag = self._get_content_etag(content) # Generating etag for the content.
                mc.add(constants.mc.ETAG_KEY % request_path, current_etag, expiry)
                cachepy_expiry = expiry if expiry != 0 else None
                cachepy.set(constants.cachepy.ETAG_KEY % request_path, current_etag, cachepy_expiry)
            else:
                #- MC has the etag let's cache it on cachepy and go on -#
                cachepy.set(constants.cachepy.ETAG_KEY % request_path, current_etag)

        browser_etag = self.request.headers['If-None-Match'] if 'If-None-Match' in self.request.headers else None

        """ Browser etag might be None but current_etag is always generated or gotten from the caches above """

        if browser_etag == current_etag:
            """ Ther user has already the content cached on his browser """
            self.response.headers['ETag'] = current_etag;
            self.error(304)
        else:
            """ No etag match so the content has to be generated and transferred to the client """
            if content is None:
                """ The content wasn't generated above so lest do it now """
                content = get_page()
            """ There is no need to generate the etag again because always is going to be generated above, either taken from cachepy or memcache
            or generated again """
            self.response.headers['ETag'] = current_etag;
            self.response.out.write(content)

    def handle_exception(self, exception, debug_mode):
        import traceback, sys, cgi

        # Log the error.
        logging.exception(exception)


        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

        self.http_no_caching()

        lines = ''.join(traceback.format_exception(*sys.exc_info()))
        exception_text = (cgi.escape(lines, quote=True))

        self.display_template('error.html', { 'debug_mode': debug_mode,
                                              'debug_mode_msg': exception_text,
                                              })

    def get(self):
        self.http_no_caching()
        self.error(404)
        self.display_template(self, '404.html')

    def post(self):
        self.http_no_caching()
        self.error(404)

    def cachepy(self, expiry=None, key_name=None, key_suffix=None):
        """
        Decorator
        expiry in seconds, None means forever.
        """
        def decorator(fn):
            cachepy_key_name = constants.cachepy.URL_KEY % (key_name or urllib.unquote(self.request.path))
            if key_suffix is not None:
                cachepy_key_name += ':' + key_suffix
            @cachepy.cacheit(cachepy_key_name, expiry)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapper
        return decorator

    def memcache(self, expiry=0, key_name=None, key_suffix=None):
        """
        Decorator
        expiry in seconds, 0 means forever.
        """
        def decorator(fn):
            mc_key_name = constants.mc.URL_KEY % (key_name or urllib.unquote(self.request.path))
            if key_suffix is not None:
                mc_key_name += ':' + key_suffix
            @mc.cacheit(mc_key_name, expiry, add_instead_of_set=True)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapper
        return decorator

    @classmethod
    def requests_limit(cls, limit_per_minute=60, ban_time=IP_BAN_TIME):
        """
        Decorator to limit the hits to a request handler per minute and ip
        """
        def decorator(fn):
            def wrapper(*args, **kwargs):
                timestamp = int(time.time())
                self = args[0]
                #- Check if the ip was banned -#
                ip_ban_key_name = constants.mc.IP_BAN % self.request.remote_addr
                ban = mc.get(ip_ban_key_name)
                if ban:
                    #- Renew the ban if it's going to expire in 1/3 of the banning time -#
                    ban_pending_time = ban_time - (timestamp - ban)
                    if ban_pending_time < (ban_time/3):
                        #- Renewing the ban because the attacker insists -#
                        mc.set(ip_ban_key_name, time.time(), ban_time)
                    self.abort(403)
                current_minute = timestamp - (timestamp%60)
                key_name = constants.mc.REQUEST_HIT_FROM_IP % (current_minute, self.request.path, self.request.remote_addr)
                #- Increases hits from an ip to a particular url -#
                counter = mc.incr(key_name)
                if counter > limit_per_minute:
                    #- Banning ip -#
                    mc.set(ip_ban_key_name, time.time(), ban_time)
                    self.abort(403)
                else:
                    return fn(*args, **kwargs)
            return wrapper
        return decorator
