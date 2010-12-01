URLecho
=======

Protocol and AppEngine service for echoing a HTTP response defined in the request URL

Overview
--------

URL echo is a HTTP-based client-server protocol for defining the HTTP response to a HTTP GET request within the request itself. The client sends JSON-formatted and URL-encoded parameters of the response that the server should return within the URL of a HTTP GET request. The server responds with a HTTP response by mirroring the parameters defined in the URL of the request thus effectively echoing the client-defined response. See the "Protocol" section for more information.

The project also provides a reference implementation of an URL echo server. The server is implemented as public, open-source and free to use AppEngine service. See the "AppEngine server" section for more information.

Purpose
-------

URL echo enables dynamic hosting of HTTP resources within a URL without need for any physical infrastructure (e.g. web servers). The reason for hosting a resource within a URL are links, the glue of the Web. A link functions as a pointer to a web resource - it is a single entity which defines both which resource should be fetched (a URL identifier of the resource) and how the resource should be fetched (HTTP GET request to that URL). Therefore, defining a resource in the URL of a HTTP request makes it widely usable in the existing web architecture by both developers and end-users. 

Want to show a web page to someone? With URL echo you wouldn't need to setup a web hosting account with a provider, upload your files to a web host and then share the URL to the web page with your friends. Instead, you would build your web page, encode it's content in a URL, and share the URL with your friends skipping the whole step of hosting. Need a fast way to create a large number of HTTP resources, for testing or other purposes? Just create the URLs containing the resources on the client side, no need for creating server-side scripts.

Since the resource are defined and contained solely within the URL, URL echo may only be used to host static HTTP resources. However, a significant percentage of all web resources are static resources and in many occasions that's enough. Also, since creating a resource is as easy as constructing a URL, this limitation is irrelevant in use cases where the resource creator has control over all links that point to that URL - a resource is changed by pointing a link at a different URL can easily change the URL of the link to change the resource.

Protocol
--------

The URL echo protocol is an extension of the [HTTP protocol](http://tools.ietf.org/html/rfc2616), specifically the HTTP GET method. With regular HTTP, when a server receives a GET request from the client, it responds with a response containing the URL-addressed resource. In most cases, this means that the resource is retreived either from a server-side script or fetched from a static file on the server. 

In contrast, the URL echo protocol functions as follows:

* **The client** sends a HTTP GET request to the server. The URL of the request contains a [JSON-formatted](http://json.org) and [URL-encoded](http://en.wikipedia.org/wiki/Percent-encoding) representation of a HTTP response object. The exact positioning of the JSON-formatted HTTP response object is up to the server implementation (e.g. as a query parameter or a part of the path). 

  The HTTP response JSON object has 3 properties:
  * status - a string representing the HTTP status code of the HTTP response
  * headers - a JSON object representing headers of the HTTP response. Each header is represented as key-value string pair of a header name and header value.
  * content - a string representing the body of the HTTP response

  All properties are optional, and in the case that any property is omitted - the server will assume default values as defined below.

  Here's an example JSON object that defines a HTTP response containing an ATOM feed in the response body:

    {
      "status" : "200",
      "headers" : { "Content-Type" : "application/atom+xml" }
      "content" : "
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
          </feed>"
    }

  And this is the URL-encoded string for the same JSON-formatted object:

    %7B%22status%22:200,%22headers%22:%7B%22Content-Type%22:%22application/atom%2Bxml%22%7D,%22content%22:%22%3C%3Fxml%20version%3D'1.0'%20encoding%3D'utf-8'%3F%3E%5Cn%20%20%20%20%20%20%3Cfeed%20xmlns%3D'http://www.w3.org/2005/Atom'%3E%5Cn%20%20%20%20%20%20%20%20%3Ctitle%3EExample%20Feed%3C/title%3E%5Cn%20%20%20%20%20%20%20%20%3Csubtitle%3EA%20subtitle.%3C/subtitle%3E%5Cn%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/feed/'%20rel%3D'self'%20/%3E%5Cn%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/'%20/%3E%5Cn%20%20%20%20%20%20%20%20%3Cid%3Eurn:uuid:60a76c80-d399-11d9-b91C-0003939e0af6%3C/id%3E%5Cn%20%20%20%20%20%20%20%20%3Cupdated%3E2003-12-13T18:30:02Z%3C/updated%3E%5Cn%20%20%20%20%20%20%20%20%3Cauthor%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cname%3EJohn%20Doe%3C/name%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cemail%3Ejohndoe@example.com%3C/email%3E%5Cn%20%20%20%20%20%20%20%20%3C/author%3E%5Cn%20%20%20%20%20%20%20%20%3Centry%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Ctitle%3EAtom-Powered%20Robots%20Run%20Amok%3C/title%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/2003/12/13/atom03'%20/%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cid%3Eurn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a%3C/id%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cupdated%3E2003-12-13T18:30:02Z%3C/updated%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Csummary%3ESome%20text.%3C/summary%3E%5Cn%20%20%20%20%20%20%20%20%3C/entry%3E%3C/feed%3E%22%7D

* **The server** receives the request, and retrieves the URL-encoded JSON-formatted JSON object from the request URL. The server then replies by copying HTTP response parameters from the retreived object defined object, thus echoing the HTTP response object defined in the request URL. 

  The server must construct the response the following way:
  * The status of the HTTP response must be copied from the `status` parameter. In case that the `status` parameter is not present, the server must default the response status to "200".
  * Headers defined in the `headers` parameter must be copied to the headers of the server's HTTP response. Headers which are not set may be set arbitrarily by the server. In case that the `headers` parameter is not present, the server must set the "Content-Type" header to "text/html" representing the a plain HTML content type.
  * The body of the HTTP response must be copied from the `content` parameter. In case that the `content` parameter is not present, the server must default the response body to an empty string.

  Here's the URL echo HTTP response for the above ATOM feed GET example:

    HTTP/1.1 200 OK
    Content-Type: application/atom+xml
    <...other-server-headers...>
    
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

AppEngine server
----------------

A public, free to use and [open-source](http://github.com/izuzak/urlecho/tree/master/src) implementation of an URL echo server is available on [AppEngine](http://code.google.com/appengine/). The use the server, build an URL-encoded JSON-formatted string as defined in the protocol section, and pass it as an URL query parameter named **`jsonResponse`** to **`http://urlecho.appspot.com/echo`**. The resulting URL should look like this:

    http://urlecho.appspot.com/echo?jsonResponse=URL_ENCODED_JSON

Here's the URL for the above ATOM feed GET example, which you can copy and paste into a new tab to see it work:

    http://urlecho.appspot.com/echo?jsonResponse=%7B%22status%22:200,%22headers%22:%7B%22Content-Type%22:%22application/atom%2Bxml%22%7D,%22content%22:%22%3C%3Fxml%20version%3D'1.0'%20encoding%3D'utf-8'%3F%3E%5Cn%20%20%20%20%20%20%3Cfeed%20xmlns%3D'http://www.w3.org/2005/Atom'%3E%5Cn%20%20%20%20%20%20%20%20%3Ctitle%3EExample%20Feed%3C/title%3E%5Cn%20%20%20%20%20%20%20%20%3Csubtitle%3EA%20subtitle.%3C/subtitle%3E%5Cn%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/feed/'%20rel%3D'self'%20/%3E%5Cn%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/'%20/%3E%5Cn%20%20%20%20%20%20%20%20%3Cid%3Eurn:uuid:60a76c80-d399-11d9-b91C-0003939e0af6%3C/id%3E%5Cn%20%20%20%20%20%20%20%20%3Cupdated%3E2003-12-13T18:30:02Z%3C/updated%3E%5Cn%20%20%20%20%20%20%20%20%3Cauthor%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cname%3EJohn%20Doe%3C/name%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cemail%3Ejohndoe@example.com%3C/email%3E%5Cn%20%20%20%20%20%20%20%20%3C/author%3E%5Cn%20%20%20%20%20%20%20%20%3Centry%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Ctitle%3EAtom-Powered%20Robots%20Run%20Amok%3C/title%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Clink%20href%3D'http://example.org/2003/12/13/atom03'%20/%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cid%3Eurn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a%3C/id%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Cupdated%3E2003-12-13T18:30:02Z%3C/updated%3E%5Cn%20%20%20%20%20%20%20%20%20%20%3Csummary%3ESome%20text.%3C/summary%3E%5Cn%20%20%20%20%20%20%20%20%3C/entry%3E%3C/feed%3E%22%7D


The service also supports a debug mode in which the response will be send as the body in text/plain. To specify debug mode, add this query parameter to the end of the request URL: `debugMode=1`.

You can also use the simple URL builder form available at: [http://izuzak.github.com/urlecho](http://izuzak.github.com/urlecho).

Advanced
--------

### URL shortening ###

URL echo URLs are long and ugly since they contain a complete web resource definition (e.g. a web page). Although the URLs are completely functional, sometims it is more practical to have a shorter version. This is a perfect use case for URL shortening services like [bit.ly](http://bit.ly). URL shortening services produce short URLs from long ones and sending a GET request to short URL redirects the request to the long URL.

For example, this is the short bit.ly version of the ATOM feed URL echo example URL: [http://bit.ly/bV0So](http://bit.ly/bV0So).
