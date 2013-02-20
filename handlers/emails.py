from base import Base

class Emails(Base):
    def _test_example(self, content_type):
        self.http_no_caching()

    	template_name = 'emails/example'
    	
        if content_type == 'html':
        	template_name += '.html'
        else:
            self.set_http_content_type('text/plain')
            template_name += '.txt'
        
        self.display_template(template_name)


    def get(self, email_name, content_type):
        method_name = "_test_%s" % email_name
        if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
            self.abort(404)
        getattr(self, method_name)(content_type)