# -*- coding: utf-8 -*-
import json

try:
    from email.header import Header
except ImportError:
    from email.Header import Header

import pytest
from six.moves.urllib.parse import urlencode

from utils import DummyExtra


GET_DATA_PARAMS = ('headers', 'params', 'extra')
GET_DATA = {
    'with no headers, param and extra': (
        {},
        {},
        object(),
    ),

    'with headers': (
        {'X-Debug': '1', 'X-Test': 'test'},
        {},
        object(),
    ),

    'with headers and param': (
        {'X-Debug': '1', 'X-Test': 'test'},
        {'data': 'test', 'num': 1},
        object(),
    ),

    'with headers and param[utf-8 encoded string]': (
        {'X-Debug': '1', 'X-Test': 'test'},
        {'データ': 'テスト', '番号': 1},
        object(),
    ),

    'with headers, param and extra': (
        {'X-Debug': '1', 'X-Test': 'test'},
        {'データ': 'テスト', '番号': 1},
        DummyExtra({'headers': ['X-Debug']}),
    ),

    'with headers, param and extra[unexisted key]': (
        {'X-Debug': '1', 'X-Test': 'test'},
        {'データ': 'テスト', '番号': 1},
        DummyExtra({'headers': ['X-Debug', 'X-Unknown']}),
    ),
}


POST_DATA_PARAMS = ('headers', 'data')
POST_DATA = {
    'with no data': (
        {'Content-Length': '0',
         'Content-Type': 'application/x-www-form-urlencoded'},
        '',
    ),

    'with x-www-form-urlencoded data and headers': (
        {'Content-Type': 'application/x-www-form-urlencoded'},
        urlencode({'data': 'test', 'num': 1}),
    ),

    'with x-www-form-urlencoded data[utf-8 encoded string] and headers': (
        {'Content-Type': 'application/x-www-form-urlencoded'},
        urlencode({'データ': 'テスト', '番号': 1}),
    ),

    'with json data and headers': (
        {'Content-Type': 'application/json', 'X-Debug': '1'},
        json.dumps({'data': 'test', 'num': 1}),
    ),

    'with json data[utf-8 encoded string] and headers': (
        {'Content-Type': 'application/json', 'X-Debug': '1'},
        json.dumps({'データ': 'テスト', '番号': 1}),
    ),
}


POST_DATA_MULTIPART_PARAMS = ('headers', 'data')
POST_DATA_MULTIPART = {
    'with multipart/form-data to send form data': (
        {'Content-Type': 'multipart/form-data'},
        {'data': (None, 'test'), 'num': (None, '1')},
    ),

    'with multipart/form-data to send attachments':
    pytest.mark.skipif('os.environ.get("DRONE")')((
        {'Content-Type': 'multipart/form-data'},
        {'attachment1': ('attach.txt', 'tests/fixtures/attach.txt'),
         'attachment2': (
            Header(u'添付.txt').encode(), 'tests/fixtures/添付.txt')},
    )),

    'with multipart/form-data to send form data and attachment': (
        {'Content-Type': 'multipart/form-data'},
        {'data': (None, 'test'),
         'attachment': ('attach.txt', 'tests/fixtures/attach.txt')},
    ),
}


PUT_DATA_PARAMS = ('headers', 'data')
PUT_DATA = {
    'with no data': (
        {'Content-Type': 'application/json'},
        '',
    ),

    'with json data and headers': (
        {'Content-Type': 'application/json'},
        json.dumps({'data': 'test', 'num': 1}),
    ),

    'with json data[utf-8 encoded string] and headers': (
        {'Content-Type': 'application/json'},
        json.dumps({'データ': 'テスト', '番号': 1}),
    ),

    'with json data and additional headers': (
        {'Content-Type': 'application/json', 'X-Debug': '1'},
        json.dumps({'データ': 'テスト', '番号': 1}),
    ),
}


DELETE_DATA_PARAMS = PUT_DATA_PARAMS
DELETE_DATA = PUT_DATA.copy()


PROXY_DATA_PARAMS = ('method', 'proxies', 'headers', 'data')
PROXY_DATA = {
    'via proxy for get request': (
        'get',
        {'http': 'http://127.0.0.1:8888', 'https': 'https://127.0.0.1:8888'},
        {'Content-Length': '0', 'X-Debug': '1'},
        {},
    ),

    'via proxy for post request': (
        'post',
        {'http': 'http://127.0.0.1:8888', 'https': 'https://127.0.0.1:8888'},
        {'Content-Type': 'application/json'},
        json.dumps({'data': 'test', 'num': 1}),
    ),
}
