# -*- coding: utf-8 -*-
import json
import logging
import os
from subprocess import Popen, PIPE

from pytest_curl_report.utils import Curl


EXCLUDE_HEADER_KEYS = [
    'Accept',
    'Accept-Encoding',
    'Connection',
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

    log.debug('remove_exclude_headers result:')
    log.debug(headers)


def assert_curl_response(request, extra, expected):
    cmd = Curl(request, extra).make_command()

    with open(os.devnull, 'w') as devnull:
        p = Popen(cmd, stdout=PIPE, stderr=devnull, shell=True)
        stdout, _ = p.communicate()
        actual = json.loads(stdout.decode('utf-8'))

    log.debug('curl command result:')
    log.debug(actual)

    remove_exclude_headers(actual['headers'], extra)
    remove_exclude_headers(expected['headers'], extra)
    assert actual == expected
