# coding: utf-8
from base import Base

class Home(Base):
    def get(self):
        self.http_no_caching()
        @self.cachepy()
        @self.memcache()
        def get_page():
            params = {'og_url': self.uri_for(self.URL.HOME, _full=True)}
            return self.get_template('home.html', params)
        self.display_page_or_304(get_page)