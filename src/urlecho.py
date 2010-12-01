import cgi
import os
import re
import urllib
import urlparse
import mimetypes

from django.utils import simplejson 
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import DownloadError 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class BaseURLEchoHandler(webapp.RequestHandler):
  def parseRequestQueryStringParams(self, requestQueryString, paramsList):
    requestQueryString = "&" + requestQueryString
    paramIndexes = [(param, requestQueryString.find('&' + param + '=')) for param in paramsList]
    paramIndexes = sorted(filter(lambda x: x[1]!=-1, paramIndexes),key=lambda x:x[1])
    paramIndexes = [(paramIndexes[i][0], paramIndexes[i][1] + len(paramIndexes[i][0]) + 2, len(requestQueryString) if (i == (len(paramIndexes)-1)) else paramIndexes[i+1][1])
                    for i in range(len(paramIndexes))]
    return dict((param[0], urllib.unquote(requestQueryString[param[1]:param[2]])) for param in paramIndexes)
	
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
    
    # process debug mode
    if isDebugMode:
      debugHeaders = {}
      debugHeaders.update(self.response.headers)
      if responseParams.has_key('headers'):
        debugHeaders.update(responseParams['headers'])
      debugHeaders.update( { 'Access-Control-Allow-Origin' : '*' } )
      self.response.set_status(200)
      self.response.headers['Content-Type'] = 'text'
      self.response.out.write("Request received:\n%s\n\n" % self.request.url)
      self.response.out.write("Status code:\n%s\n\n" % (str(responseParams['status']) if responseParams.has_key('status') else "200"))
      self.response.out.write("Headers:\n%s\n\n" % "\n".join( item[0] + ": " + item[1] for item in debugHeaders.items()))
      self.response.out.write("Content:\n%s" % responseParams['content'])
    else:
      # process status
      if responseParams.has_key('status'):
        self.response.set_status(responseParams['status'])
      
      # process headers
      if responseParams.has_key('headers'):
        for headerName in responseParams['headers'].keys():
          self.response.headers[headerName] = responseParams['headers'][headerName]
      
      # process content
      if responseParams.has_key('content'):
        self.response.out.write(responseParams['content'])
    
    return

class JsonStringURLEchoHandler(BaseURLEchoHandler):
  def parseResponseParams(self, queryString):
    requestParams = self.parseRequestQueryStringParams(queryString, ['jsonResponse', 'debugMode'])
    
    responseParams = {}
    if requestParams.has_key('jsonResponse'):
      responseParams = simplejson.loads(requestParams['jsonResponse'])
    
    isDebugMode = requestParams.has_key('debugMode') and requestParams['debugMode'] == "1"
    return responseParams, isDebugMode

class URLGadgetHandler(BaseURLEchoHandler):
  UrlGadgetTemplate = '<?xml version="1.0" encoding="UTF-8" ?><Module><ModulePrefs title="URL Gadget generated by UrlEcho service for %s" />  <Content type="url" href="%s"></Content></Module>'

  def parseResponseParams(self, queryString):
    responseParams = {}
    requestParams = self.parseRequestQueryStringParams(queryString, ['destinationUrl', 'debugMode'])
    responseParams['content'] = URLGadgetHandler.UrlGadgetTemplate % (requestParams['destinationUrl'], requestParams['destinationUrl'])
    isDebugMode = requestParams.has_key('debugMode') and requestParams['debugMode'] == "1"
    return responseParams, isDebugMode

class QueryStringHandler(BaseURLEchoHandler):  
  def parseResponseParams(self, queryString):
    responseParams = {}
    
    requestParams = self.parseRequestQueryStringParams(queryString, ['status','headers','content','debugMode'])
    
    # parse status
    if requestParams.has_key('status'):
      responseParams['status'] = int(requestParams['status'])
    
    # parse headers
    if requestParams.has_key('headers'):
      headers = requestParams['headers'].split("&")
      responseParams['headers'] = dict(map(lambda x: map(urllib.unquote, x.split("=", 1)), headers))
    
    # process content
    if requestParams.has_key('content'):
      responseParams['content'] = requestParams['content']
    
    isDebugMode = requestParams.has_key('debugMode') and requestParams['debugMode'] == "1"
    return responseParams, isDebugMode
    
class RedirectToGoogleCodeHandler(webapp.RequestHandler):
  def get(self):
    self.redirect('http://github.com/izuzak/urlecho')

application = webapp.WSGIApplication([('/generateUrlGadget.*', URLGadgetHandler),
                                      ('/echoqueryparams.*', QueryStringHandler),
                                      ('/echo.*', JsonStringURLEchoHandler),
                                      ('/.*', RedirectToGoogleCodeHandler)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
