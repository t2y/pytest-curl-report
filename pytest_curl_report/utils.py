# -*- coding: utf-8 -*-
import os


class BaseRequest(object):

    def get_proxy_settings(self, url):
        http_proxy = os.environ.get('HTTP_PROXY')
        https_proxy = os.environ.get('HTTPS_PROXY')
        if http_proxy and url.startswith('http:'):
            return http_proxy.replace('http://', '')
        elif https_proxy and url.startswith('https:'):
            return https_proxy.replace('https://', '')
        return None


class UrllibRequest(BaseRequest):

    def __init__(self, request):
        self.url = request.get_full_url()
        self.method = request.get_method()
        self.proxy = self.get_proxy_settings(self.url)
        self.headers = request.headers

        self.data = ''
        if request.data:
            self.data = request.data.decode('utf-8')

        self._request = request


class RequestsRequest(BaseRequest):

    def __init__(self, request):
        self.url = request.url
        self.proxy = self.get_proxy_settings(self.url)
        self.method = request.method
        self.headers = request.headers

        if hasattr(request, 'body'):
            self.data = request.body
        else:
            self.data = request.data

        self._request = request


def get_inspect_functions():
    funcs = []
    if has_requests():
        funcs.append(get_requests_request)

    funcs.append(get_urllib_request)
    return funcs


def get_urllib_request(obj):
    try:
        from urllib.request import Request
    except ImportError:
        from urllib2 import Request

    if isinstance(obj, Request):
        return UrllibRequest(obj)

    return None


def has_requests():
    try:
        import requests.models  # pragma: no flakes
    except ImportError:
        return False
    else:
        return True


def get_requests_request(obj):
    from requests.models import Response
    from requests.models import Request as ReqRequest, PreparedRequest

    if isinstance(obj, Response):
        return RequestsRequest(obj.request)
    elif isinstance(obj, (ReqRequest, PreparedRequest)):
        return RequestsRequest(obj)

    return None
