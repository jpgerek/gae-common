# coding: utf-8
import hashlib
import config
import logging
from google.appengine.api import urlfetch
import json
import config
import urllib2
import constants
import webapp2

def retry( retries=3 ):
    """ Retries the decorated function till no exception is raised or the retries are over """
    def decorator( func ):
        def wrapper( *args, **kwargs ):
            #Make the value mutable, this is required to be able to use the retries var above
            _retries=retries
            while True:
                try:
                    result = func( *args, **kwargs )
                    return result
                except:
                    _retries -= 1
                    if _retries == 0:
                        raise
        return wrapper
    return decorator

def sha1(text):
    #Some strings crash, as temporal solution I add ignoring the bad characters it works, but it's not correct.
    return hashlib.sha1(text).hexdigest()

def md5hex(text):
    md5 = hashlib.md5(text)
    return md5.hexdigest()

def add_email_to_queue( to, subject, body, html ):
    add_task_to_queue('emails', '/tasks/email', {
        'to': to,
        'subject': subject,
        'body': body,
        'html': html,
        });


def send_email(to, subject, body, html):
    from google.appengine.api import mail
    import mc
    sender = config.EMAIL_SENDER
    error = False
    if config.DEVELOPMENT:
        logging.info('Mail send: %s - %s - %s - %s' % (subject, to, body, html))
    else:
        count = mc.incr(constants.mc.EMAIL_COUNTER)
        logging.info('Sending email to "%s", count: %d' % (to, count))
        if (count%3) == 0:
            #- Appengine free quota is 100 emails per day -#
            msg = mail.EmailMessage()
            msg.sender = sender
            subject = config.EMAIL_SUBJECT_PREFIX + subject
            msg.subject = subject
            msg.to = to
            msg.body = body
            msg.html = html
            error = not msg.is_initialized()
            msg.send()
        else:
            #- Sendgrid free quota is 200 emails per day -#
            to = to.split(' ')[0]
            to_name = ''
            error = not send_email_using_sendgrid(to, to_name, subject, body, html)
    if error:
        logging.error('Error sending the email: %s - %s - %s - %s -%s' % ( sender, to, subject, body, html ))

def send_email_using_sendgrid(to, to_name, subject, text, html):
    import urllib
    url = "https://sendgrid.com/api/mail.send.json"
    payload = {
                'api_user': config.SENGRID_USERNAME,
                'api_key': config.SENGRID_API_KEY,
                'to': to,
                'toname': to_name,
                'subject': subject,
                'text': text,
                'html': html,
                'from': config.EMAIL_SENDER,
                'fromname': config.EMAIL_SENDER_NAME
            }
    #- Apply hack to solve the unicode problems -#
    for key, value in payload.iteritems():
        payload[key] = (u"%s" % value).encode('utf-8')

    encoded_payload = urllib.urlencode(payload)
    result = urlfetch.fetch(url, payload=encoded_payload, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if result.status_code == 200:
        result_json = json.loads(result.content)
        if result_json['message'] == 'success':
            return True
    return False

@retry()
def add_task_to_queue(queue_name, url, params  = {}):
    from google.appengine.api.labs.taskqueue import Queue, Task

    task = Task(url=url, params=params)
    Queue(queue_name).add(task)

@retry()
def shorten_url(url):
    url_request = "http://api-ssl.bitly.com/v3/shorten?login=%s&apiKey=%s&longUrl=%s"\
                  % (urllib2.quote(config.BITLY_USERNAME), urllib2.quote(config.BITLY_APIKEY), urllib2.quote(url))
    result = urlfetch.fetch(url_request)
    if result.status_code == 200:
        result_json = json.loads(result.content)
        if result_json['status_code'] == 200:
            return result_json['data']['url']
        if result_json['status_txt'] == 'INVALID_URI':
            #- It probably means we are in local environment and localhost is not a valid domain -#
            return url
    #- Raise any exception so the retry decorators tries again -#
    raise Exception

def add_email_to_queue( to, subject, body, html ):
    add_task_to_queue('emails', webapp2.uri_for(constants.url.tasks.SEND_EMAIL), {
        'to': to,
        'subject': subject,
        'body': body,
        'html': html,
        });