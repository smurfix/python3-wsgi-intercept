"""
intercept HTTP connections that use httplib or http.client
"""

try:
    import http.client as http_lib
except ImportError:
    import httplib as http_lib

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection

try:
    from http.client import (
            HTTPConnection as OriginalHTTPConnection,
            HTTPSConnection as OriginalHTTPSConnection
    )
except ImportError:
    from httplib import (
            HTTPConnection as OriginalHTTPConnection,
            HTTPSConnection as OriginalHTTPSConnection
    )

HTTPInterceptorMixin = WSGI_HTTPConnection
HTTPSInterceptorMixin = WSGI_HTTPSConnection
    
def install():
    class HTTP_WSGIInterceptor(HTTPInterceptorMixin, http_lib.HTTPConnection):
        pass
    
    class HTTPS_WSGIInterceptor(HTTPSInterceptorMixin, http_lib.HTTPSConnection,
            HTTP_WSGIInterceptor):
    
        def __init__(self, host, **kwargs):
            self.host = host
            try:
                self.port = kwargs['port']
            except KeyError:
                self.port = None
            HTTP_WSGIInterceptor.__init__(self, host, **kwargs)

    http_lib.HTTPConnection = HTTP_WSGIInterceptor
    http_lib.HTTPSConnection = HTTPS_WSGIInterceptor
    http_lib.HTTP._connection_class = HTTP_WSGIInterceptor


def uninstall():
    http_lib.HTTPConnection = OriginalHTTPConnection
    http_lib.HTTPSConnection = OriginalHTTPSConnection
    http_lib.HTTP._connection_class = OriginalHTTPConnection
