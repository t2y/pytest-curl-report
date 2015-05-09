# -*- coding: utf-8 -*-
import json

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
        {'Content-Type': 'application/x-www-form-urlencoded'},
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
