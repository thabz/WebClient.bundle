import Framework

@handler('/plugins/webproxy', 'Web Proxy')
def Main():
  pass

@route('/plugins/webproxy/request', method=('GET', 'POST', 'PUT', 'DELETE'))
def ProxyRequest():
  # Copy the request headers.
  headers = dict(Request.Headers)

  # Grab the real URL from the header dict.
  url = headers['X-Plex-Url']
  del headers['X-Plex-Url']

  # Whack unwanted request headers.
  if 'Host' in headers:
    del headers['Host']

  # Make the HTTP request.
  req = HTTP.Request(
    url = url,
    method = Request.Method,
    headers = headers,
    data = Request.Body if Request.Body and len(Request.Body) > 0 else None,
    immediate = True
  )

  # Whack unwanted response headers. In particular, the original response
  # may have been gzipped, but this response won't be.
  headers = {}
  for name in req.headers:
    headers[name] = req.headers[name]
  for name in ['content-encoding', 'content-length', 'transfer-encoding']:
    if name in headers:
      del headers[name]

  # Replace a couple headers in a hacky way, since case matters
  if 'cache-control' in headers:
    headers['Cache-Control'] = headers['cache-control']
    del headers['cache-control']
  if 'content-type' in headers:
    headers['Content-type'] = headers['content-type']
    del headers['content-type']

  # Update the response headers.
  for name in headers:
    Response.Headers[name] = headers[name]

  # Return the response body.
  return req.content
