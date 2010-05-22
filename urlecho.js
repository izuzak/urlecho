var urlecho = function() {

  function getEchoURL(params) {
    var urlEncodedJson =  encodeURIComponent(JSON.stringify({"status" : params.status, "headers" : params.headers, "content" : params.content })); 
    var subdomain = (typeof params.subdomain === "undefined" || params.subdomain === null || params.subdomain === "") ? "" : params.subdomain + ".";
    var outputUrl = "http://" + subdomain + "urlecho.appspot.com/echo?jsonResponse=" + urlEncodedJson;
    return outputUrl;
  }
  
  return {
    getEchoURL : getEchoURL
  };
}();