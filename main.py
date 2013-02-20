# coding: utf-8
import webapp2
import config
from constants import url
from validation import custom_base64_regex, base64_regex

config_dict = config.__dict__

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler='handlers.Home', name=url.HOME, methods=['GET']),
    webapp2.Route(r'/emails/<email_name:[a-zA-Z0-9_]+>/<content_type:(txt|html)>', handler='handlers.Emails', name= url.EMAILS, methods=['GET']),
    webapp2.Route('/tasks/' + url.tasks.SEND_EMAIL, handler='handlers.tasks.SendEmail', name=url.tasks.SEND_EMAIL, methods=['POST']),
    webapp2.Route(r'/<path>', handler='handlers.PageNotFound', methods=['POST'])
], debug=config.DEVELOPMENT, config=config_dict)
