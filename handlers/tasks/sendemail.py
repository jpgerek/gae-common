from handlers import Base
import helpers

class SendEmail(Base):
    def post(self):
        to = self.request.get('to')
        subject = self.request.get('subject')
        body = self.request.get('body')
        html = self.request.get('html')
        helpers.send_email(to, subject, body, html)