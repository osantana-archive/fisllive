from os.path import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}

        path = join(dirname(__file__), 'index.html')
        rendered = template.render(path, template_values)
        self.response.out.write(rendered)

if __name__ == "__main__":
    application = webapp.WSGIApplication([
        ('/', MainHandler)
    ], debug=True)
    util.run_wsgi_app(application)
