"""
intercept HTTP connections that use requests
"""

from . import WSGI_HTTPConnection, WSGI_HTTPSConnection, wsgi_fake_socket
try:
    from requests.packages.urllib3 import connectionpool
except ImportError:
    from urllib3 import connectionpool

HTTPConnection = connectionpool.HTTPConnection
HTTPSConnection = connectionpool.HTTPSConnection

InterceptorMixin = WSGI_HTTPConnection
InterceptorMixinS = WSGI_HTTPSConnection
wsgi_fake_socket.settimeout = lambda self, timeout: None


def install():
    connectionpool.HTTPConnection = InterceptorMixin
    connectionpool.HTTPSConnection = InterceptorMixinS


def uninstall():
    connectionpool.HTTPConnection = HTTPConnection
    connectionpool.HTTPSConnection = HTTPSConnection
