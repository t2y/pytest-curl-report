# -*- coding: utf-8 -*-
import json


class UrllibRequest(object):

    def __init__(self, request):
        self.url = request.get_full_url()
        self.method = request.get_method()
        self.headers = request.headers
        self.data = ''
        if request.data:
            self.data = request.data.decode('utf-8')
        self._request = request


class RequestsRequest(object):

    def __init__(self, request):
        self.url = request.url
        self.method = request.method
        self.headers = request.headers
        if hasattr(request, 'body'):
            self.data = request.body
        else:
            self.data = request.data
        self._request = request


class Curl(object):

    def __init__(self, request, extra):
        self.url = request.url
        self.method = request.method
        self.headers = request.headers
        self.lower_headers = dict(
            [(k.lower(), v.lower()) for k, v in request.headers.items()]
        )
        self.data = request.data
        self.extra = extra

    @property
    def command_template(self):
        if self.method == 'GET':
            return 'curl -X %(method)s %(headers)s "%(url)s"'
        else:
            return 'curl -X %(method)s %(headers)s %(data)s "%(url)s"'

    def get_header_params(self):
        header_keys = getattr(self.extra, 'headers', None)
        if header_keys is None:
            headers = self.headers
        else:
            headers = dict(
                (k, self.lower_headers.get(k.lower(), '')) for k in header_keys
            )
        return ' '.join('-H "%s: %s"' % (k, v) for k, v in headers.items())

    def get_data_params(self):
        if self.method == 'GET':
            return ''

        content_type = self.lower_headers.get('content-type', '')
        if content_type.startswith('application/json'):
            return '-d %s' % json.dumps(self.data)

        if isinstance(self.data, dict):
            return ' '.join(
                '-d "%s: %s"' % (k, v) for k, v in self.data.items()
            )

        return '-d "%s"' % self.data

    def make_command(self):
        return self.command_template % {
            'url': self.url,
            'method': self.method,
            'headers': self.get_header_params(),
            'data': self.get_data_params(),
        }


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
