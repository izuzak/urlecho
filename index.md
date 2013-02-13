---
layout: default
title: URL Echo
description: HTTP service for echoing the HTTP response defined in the URL of the request
github_url: https://github.com/izuzak/urlecho
ga_tracking: UA-9935885-1

---

Overview
--------

URL Echo is an HTTP service for echoing the HTTP response defined in the URL of the request.

The service expects a definition of a HTTP response message in the URL of a request to the service. The service responds with a HTTP response by mirroring the parameters defined in the URL of the request thus echoing the client-defined response.

The URL Echo service is implemented and provided as public, open-source and free to use [AppEngine](http://code.google.com/appengine/) service.

Service API
-----------

The service is available at this URL: `http://urlecho.appspot.com/echo`.

The API defines how a HTTP response should be encoded in the service request URLs. Elements of a HTTP response are encoded as URL query parameters:

  * (optional) HTTP status - `status` parameter; a number representing the HTTP status code of the HTTP response (e.g. `status=200`). Default value: `200`.
  * (optional, multiple) HTTP headers - multiple query parameters specified as `headerName=headerValue` (e.g. `Content-Type=text/plain`). Default values: `Content-Type=text/plain`
  * (optional) HTTP body - `body` parameter; a string representing the body of the HTTP response (e.g. `body=HelloWorld`).
  * (optional) debug mode - `debugMode` parameter; specifies debug mode in which the response is sent as the body in text/plain (e.g. `debugMode=1`)

URL builder
-----------

Instead of constructing URLs by hand, use the handy form below.

<div>
  <script type="text/javascript">
  String.prototype.trim = function () {
    return this.replace(/^\s*(\S*(\s+\S+)*)\s*$/, "$1");
  };

  var urlecho = function() {

    function getEchoURL(params) {
      var subdomain = (typeof params.subdomain === "undefined" || params.subdomain === null || params.subdomain === "") ? "" : params.subdomain + ".";
      var outputUrl = "http://" + subdomain + "urlecho.appspot.com/echo?";

      requrl += "status=" + params.status;

      if (params.headers) {
        for (var key in params.headers) {
          requrl += "&" + encodeURIComponent(key) + "=" + encodeURIComponent(params.headers[key]);
        }
      }

      if (params.body) {
        requrl += "&body=" + encodeURIComponent(params.body);
      }

      return outputUrl;
    }

    return {
      getEchoURL : getEchoURL
    };
  }();

  function generate() {
    _gaq.push(['_trackEvent', 'URL builder', 'createURL'])

    var responseStatus = document.getElementById("responseStatus").value;

    var responseHeaders = document.getElementById("responseHeaders").value.split("\n");
    var responseHeadersObject = {};
    for (var i=0; i<responseHeaders.length; i++) {
      var hdr = responseHeaders[i].split(":");
      responseHeadersObject[hdr[0].trim()] = hdr[1].trim();
    }

    var responseBody = document.getElementById("responseBody").value;

    var params = {
      "status" : parseInt(responseStatus),
      "headers" : responseHeadersObject,
      "body" : responseBody,
      "subdomain" : document.getElementById("subdomain").value
    };

    var outputUrl = urlecho.getEchoURL(params);
    var outputTestingUrl = outputUrl + "&debugMode=1";

    document.getElementById("outputUrl").value = outputUrl;

    var outputUrlText = outputUrl.length > 60 ? outputUrl.substring(0,57) + "..." : outputUrl;
    var testingUrlText = outputTestingUrl.length > 60 ? outputTestingUrl.substring(0,57) + "..." : outputTestingUrl;
    document.getElementById("navigateToURL").innerHTML = "Click the following link to navigate the generated URL:<br><a target=\"_blank\" href=\"" + outputUrl + "\" >" + outputUrlText + "</a>";
    document.getElementById("testingURL").innerHTML = "Click the following link to see the complete HTTP response:<br><a target=\"_blank\" href=\"" + outputTestingUrl + "\" >" + testingUrlText + "</a>";
  }
  </script>
</div>

<div id="wikicontent"> <p>
<b><label for="responseStatus">Response status code:</label></b></p><p>
<input style="width:300px; font-family:monospace" name="responseStatus" id="responseStatus" type="text" value="200"/>

</p><p><label for="responseHeaders"><b>Response headers (one per line)</b>:</label></p><p>
<textarea id="responseHeaders" name="responseHeaders" style="width:300px" rows="5" cols="20">Content-Type: text/html</textarea>

</p><p><label for="responseBody"><b>Response body</b>:</label></p><p>
<textarea id="responseBody" name="responseBody" style="width:300px" rows="10" cols="20">Hello world!</textarea>

</p><p><label for="subdomain"><b>Request URL subdomain (optional)</b>:</label></p><p>
<input style="width:300px; font-family:monospace" name="subdomain" id="subdomain" type="text" value=""/>

</p><p><button style="width:300px" name="genBtn" id="genBtn" onclick="generate();">Generate URL</button>

</p><p><b><label for="outputUrl">Output URL echo URL (select all, then copy):</label></b></p><p>
<input style="width:300px" name="outputUrl" id="outputUrl" type="text" value="">
</p>
<div id="navigateToURL">
</div><br>
<div id="testingURL">
</div>
</div>

Example
-------

Here's an example URL Echo request that defines a HTTP response containing an ATOM feed in the response body:

    http://urlecho.appspot.com/echo?status=200&body=<?xml%20version='1.0'%20encoding='utf-8'?>%20<feed%20xmlns='http://www.w3.org/2005/Atom'>%20<title>Example%20Feed</title>%20<subtitle>A%20subtitle.</subtitle>%20<link%20href='http://example.org/feed/'%20rel='self'%20/>%20<link%20href='http://example.org/'%20/>%20<id>urn:uuid:60a76c80-d399-11d9-b91C-0003939e0af6</id>%20<updated>2003-12-13T18:30:02Z</updated>%20<author>%20<name>John%20Doe</name>%20<email>johndoe@example.com</email>%20</author>%20<entry>%20<title>Atom-Powered%20Robots%20Run%20Amok</title>%20<link%20href='http://example.org/2003/12/13/atom03'%20/>%20<id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>%20<updated>2003-12-13T18:30:02Z</updated>%20<summary>Some%20text.</summary>%20</entry>%20</feed>&Content-Type=application/atom+xml

And here's the URL Echo HTTP response for the above ATOM feed GET example:

    HTTP/1.1 200 OK
    Content-Type: application/atom+xml
    <...other-headers...>

    <?xml version='1.0' encoding='utf-8'?>
    <feed xmlns='http://www.w3.org/2005/Atom'>
      <title>Example Feed</title>
      <subtitle>A subtitle.</subtitle>
      <link href='http://example.org/feed/' rel='self' />
      <link href='http://example.org/' />
      <id>urn:uuid:60a76c80-d399-11d9-b91C-0003939e0af6</id>
      <updated>2003-12-13T18:30:02Z</updated>
      <author>
        <name>John Doe</name>
        <email>johndoe@example.com</email>
      </author>
      <entry>
        <title>Atom-Powered Robots Run Amok</title>
        <link href='http://example.org/2003/12/13/atom03' />
        <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
        <updated>2003-12-13T18:30:02Z</updated>
        <summary>Some text.</summary>
      </entry>
    </feed>

Purpose
-------

URL echo enables dynamic hosting of HTTP resources within a URL without need for any physical infrastructure (e.g. web servers). The reason for hosting a resource within a URL are links, the glue of the Web. A link functions as a pointer to a web resource - it is a single entity which defines both which resource should be fetched (a URL identifier of the resource) and how the resource should be fetched (HTTP GET request to that URL). Therefore, defining a resource in the URL of a HTTP request makes it widely usable in the existing web architecture by both developers and end-users.

Want to show a web page to someone? With URL echo you wouldn't need to setup a web hosting account with a provider, upload your files to a web host and then share the URL to the web page with your friends. Instead, you would build your web page, encode it's content in a URL, and share the URL with your friends skipping the whole step of hosting. Need a fast way to dynamically create a large number of HTTP resources, for testing or other purposes? Just create the URLs containing the resources on the client side, no need for creating server-side scripts.

Since the resource are defined and contained solely within the URL, URL echo may only be used to host static HTTP resources. However, a significant percentage of all web resources are static resources and in many occasions that's enough. Also, since creating a resource is as easy as constructing a URL, this limitation is irrelevant in use cases where the resource creator has control over all links that point to that URL - a resource is changed by pointing a link at a different URL can easily change the URL of the link to change the resource.

Advanced
--------

### URL shortening ###

URL Echo URLs are long and ugly since they contain a complete web resource definition (e.g. a web page). Although the URLs are completely functional, sometims it is more practical to have a shorter version. This is a perfect use case for URL shortening services like [bit.ly](http://bit.ly). URL shortening services produce short URLs from long ones and sending a HTTP request to short URL redirects the request to the long URL.

For example, this is the short bit.ly version of the ATOM feed URL echo example URL: [http://bit.ly/bV0So](http://bit.ly/bV0So).

Credits
-------

URL Echo is developed by [Ivan Zuzak](http://ivanzuzak.info) &lt;izuzak@gmail.com&gt;.

License
-------

Licensed under the [Apache 2.0 License](https://github.com/izuzak/urlecho/blob/master/LICENSE).
