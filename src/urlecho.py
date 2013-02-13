import cgi
import os
import re
import urllib
import urlparse
import mimetypes
import webapp2

from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import DownloadError
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class BaseURLEchoHandler(webapp2.RequestHandler):
  def options(self):
    if self.request.headers.has_key('Access-Control-Request-Method'):
      self.response.set_status(200)
      self.response.headers['Access-Control-Allow-Origin'] = self.request.headers['Origin']
      self.response.headers['Access-Control-Max-Age'] = 3600
      self.response.headers['Access-Control-Allow-Methods'] = self.request.headers['Access-Control-Request-Method']
    else:
      self.processRequest()
    return

  def get(self):
    self.processRequest()
    return

  def put(self):
    self.processRequest()
    return

  def post(self):
    self.processRequest()
    return

  def delete(self):
    self.processRequest()
    return

  def head(self):
    self.processRequest()
    return

  def processRequest(self):
    responseParams, isDebugMode = self.parseResponseParams(self.request.query_string)

    # cache all results if not requested otherwise
    if not responseParams.has_key('Cache-Control'):
      self.response.headers['Cache-Control'] = 'max-age=3600'

    if not responseParams.has_key('Access-Control-Allow-Origin'):
      self.response.headers['Access-Control-Allow-Origin'] = '*'

    # process debug mode
    if isDebugMode:
      debugHeaders = {}
      debugHeaders.update(self.response.headers)
      if responseParams.has_key('headers'):
        debugHeaders.update(responseParams['headers'])
      self.response.set_status(200)
      self.response.headers['Content-Type'] = 'text/plain'

      self.response.out.write("Request received:\n%s\n\n" % self.request.url)

      self.response.out.write("Status code:\n%s\n\n" % (str(responseParams['status']) if responseParams.has_key('status') else "200"))

      self.response.out.write("Headers:\n");

      for item in debugHeaders.items():
        self.response.out.write(item[0] + ": " + item[1] + "\n")

      self.response.out.write("\nBody:\n%s" % responseParams['body'])
    else:
      # process status
      if responseParams.has_key('status'):
        self.response.set_status(responseParams['status'])

      # process headers
      if responseParams.has_key('headers'):
        for headerName in responseParams['headers'].keys():
          self.response.headers[headerName] = responseParams['headers'][headerName]

      # process content
      if responseParams.has_key('body'):
        self.response.out.write(responseParams['body'])

    return

class QueryStringHandler(BaseURLEchoHandler):
  def parseResponseParams(self, queryString):
    responseParams = {}

    parsedQs = cgi.parse_qs(queryString)
    params = {}
    isDebugMode = False

    params['status'] = 200
    params['headers'] = {}
    params['body'] = None

    for header in parsedQs:
      if header == "status":
        params['status'] = int(urllib.unquote(parsedQs['status'][0]))
      elif header == "debugMode":
        isDebugMode = urllib.unquote(parsedQs['debugMode'][0]) == "1"
      elif header == 'body':
        params['body'] = urllib.unquote(parsedQs['body'][0])
      else:
        params['headers'][urllib.unquote(header)] = urllib.unquote(parsedQs[header][0])

    return params, isDebugMode

class RedirectToGoogleCodeHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('http://github.com/izuzak/urlecho')

app = webapp2.WSGIApplication([('/echo.*', QueryStringHandler),
                               ('/.*', RedirectToGoogleCodeHandler)], debug=True)
