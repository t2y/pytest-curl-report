# -*- coding: utf-8 -*-
import json
import re

from .utils import BaseRequest


class Curl(object):

    def __init__(self, request, extra):
        assert isinstance(request, BaseRequest)

        self.url = request.url
        self.method = request.method
        self.headers = request.headers
        self.lower_headers = dict(
            [(k.lower(), v) for k, v in request.headers.items()]
        )
        self.data = request.data
        self.proxy = request.proxy
        self.extra = extra

    @property
    def command_template(self):
        base = 'curl -X %(method)s %(proxy)s %(headers)s'
        if self.method == 'GET':
            return base + ' "%(url)s"'
        else:
            return base + ' %(data)s "%(url)s"'

    def remove_header(self, headers, keys):
        target = [k for k in headers.keys() if k.lower() in keys]
        for key in target:
            headers.pop(key)

    def get_header_params(self):
        header_keys = getattr(self.extra, 'headers', None)
        if header_keys is None:
            headers = self.headers
        else:
            headers = dict(
                (k, self.lower_headers.get(k.lower(), '')) for k in header_keys
            )

        content_type = self.lower_headers.get('content-type', '')
        if content_type.startswith('multipart/form-data'):
            self.remove_header(headers, ['content-type', 'content-length'])

        return ' '.join('-H "%s: %s"' % (k, v) for k, v in headers.items())

    def get_data_params(self):
        if self.method == 'GET' or not self.data:
            return ''

        content_type = self.lower_headers.get('content-type', '')
        if content_type.startswith('application/json'):
            return '-d %s' % json.dumps(self.data)

        if content_type.startswith('multipart/form-data'):
            options = []
            formdata, filenames = parse_multipart_data(self.data, content_type)
            if filenames:
                for info in filenames:
                    name = info['name']
                    options.append('-F "%s=@%s"' % (name, info['filename']))
                    formdata.pop(name)

            for key, values in formdata.items():
                for value in values:
                    options.append('-F "%s=%s"' % (key, value.decode('utf-8')))

            return ' '.join(options)

        if isinstance(self.data, dict):
            return ' '.join(
                '-d "%s: %s"' % (k, v) for k, v in self.data.items()
            )

        return '-d "%s"' % self.data

    def get_proxy_params(self):
        if self.proxy is not None:
            return '-x %s' % self.proxy
        return ''

    def make_command(self):
        command = self.command_template % {
            'url': self.url,
            'method': self.method,
            'headers': self.get_header_params(),
            'data': self.get_data_params(),
            'proxy': self.get_proxy_params(),
        }
        return command.replace('  ', ' ')


def get_boundary_string(content_type):
    boundary = '------unknown'
    split = content_type.split(';')
    if len(split) > 1:
        boundary = split[1].strip().split('=')[1].strip()
    return {'boundary': boundary.encode('utf-8')}


_RE_FILENAME = re.compile(r'name="(.+?)";\s*?filename="(.+?)"', re.M)


def parse_multipart_data(data, content_type):
    from cgi import parse_multipart
    from io import BytesIO

    try:
        from email.header import decode_header
    except ImportError:
        from email.Header import decode_header

    boundary = get_boundary_string(content_type)
    formdata = parse_multipart(BytesIO(data), boundary)

    filenames = []
    # FIXME: data should be handled as byte strings to retrive filename
    try:
        decoded_data = data.decode('utf-8')
    except:
        pass  # cannot decode if data is binary file like an image
    else:
        _filenames = re.findall(_RE_FILENAME, decoded_data)
        if _filenames:
            for name, raw_fname in _filenames:
                fname, charset = decode_header(raw_fname)[0]
                if charset is not None:
                    fname = fname.decode(charset)
                filenames.append({'name': name, 'filename': fname})

    return formdata, filenames
