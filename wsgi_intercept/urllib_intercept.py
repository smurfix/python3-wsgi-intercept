
try:
    import urllib.request as url_lib
except ImportError:
    import urllib2 as url_lib

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection

HTTPInterceptorMixin = WSGI_HTTPConnection
HTTPSInterceptorMixin = WSGI_HTTPSConnection

def install_opener():
    class WSGI_HTTPHandler(url_lib.HTTPHandler):
        """
        Override the default HTTPHandler class with one that uses the
        WSGI_HTTPConnection class to open HTTP URLs.
        """
        def http_open(self, req):
            return self.do_open(HTTPInterceptorMixin, req)
    
    
    class WSGI_HTTPSHandler(url_lib.HTTPSHandler):
        """
        Override the default HTTPSHandler class with one that uses the
        WSGI_HTTPConnection class to open HTTPS URLs.
        """
        def https_open(self, req):
            return self.do_open(HTTPSInterceptorMixin, req)
    
    
    handlers = [WSGI_HTTPHandler()]
    if WSGI_HTTPSHandler is not None:
        handlers.append(WSGI_HTTPSHandler())
    opener = url_lib.build_opener(*handlers)
    url_lib.install_opener(opener)


def uninstall_opener():
    url_lib.install_opener(None)
