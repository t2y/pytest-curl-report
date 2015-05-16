# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import threading
import time
from subprocess import Popen, PIPE

from pytest_curl_report.curl import Curl


EXCLUDE_HEADER_KEYS = [
    'Accept',
    'Accept-Encoding',
    'Connection',
    'Expect',
    'Proxy-Connection',
    'User-Agent',
]

log = logging.getLogger(__name__)


class DummyExtra(object):

    def __init__(self, extra):
        for key, value in extra.items():
            setattr(self, key, value)


def remove_exclude_headers(headers, extra):
    for key in EXCLUDE_HEADER_KEYS:
        headers.pop(key, None)

    header_keys = getattr(extra, 'headers', None)
    if header_keys is not None:
        keys = [key for key in headers if key not in header_keys]
        for key in keys:
            headers.pop(key, None)

    content_type = headers.get('Content-Type', '')
    if content_type.startswith('multipart/form-data'):
        headers['Content-Type'] = 'multipart/form-data'
        headers.pop('Content-Length')

    log.debug('remove_exclude_headers result:')
    log.debug(headers)


_IS_PROXY_STARTED = False


def run_proxy_server():
    import pyproxy

    global _IS_PROXY_STARTED
    if not _IS_PROXY_STARTED:
        _IS_PROXY_STARTED = True
        # HACK: remove sys.argv since tornado in pyproxy uses it
        sys.argv = []
        proxy_thread = threading.Thread(target=pyproxy.main)
        proxy_thread.daemon = True
        proxy_thread.start()
        time.sleep(1)


def assert_curl_response(request, extra, expected):
    cmd = Curl(request, extra).make_command()

    with open(os.devnull, 'w') as devnull:
        p = Popen(cmd, stdout=PIPE, stderr=devnull,
                  executable='/bin/bash', shell=True)
        stdout, _ = p.communicate()
        actual = json.loads(stdout.decode('utf-8'))

    log.debug('curl command result:')
    log.debug(actual)

    remove_exclude_headers(actual['headers'], extra)
    remove_exclude_headers(expected['headers'], extra)
    assert actual == expected
