from base import Base

class PageNotFound(Base):
    def get(self, path):
        self.error(404)
        @self.cachepy()
        @self.memcache()
        def get_page():
            return self.get_template('404.html')
        self.response.write(get_page())

    def post(self, path):
        self.error(404)
        @self.cachepy()
        @self.memcache()
        def get_page():
            return self.get_template('404.html')
        self.response.write(get_page())
