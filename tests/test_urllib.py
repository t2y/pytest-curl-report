# -*- coding: utf-8 -*-
import json
import os
import logging

import pytest
from six.moves.urllib.parse import quote
from six.moves.urllib.request import Request
from six.moves.urllib.request import urlopen

from pytest_curl_report.utils import UrllibRequest

from data import GET_DATA, GET_DATA_PARAMS
from data import POST_DATA, POST_DATA_PARAMS
from data import PROXY_DATA, PROXY_DATA_PARAMS

from utils import assert_curl_response, run_proxy_server


log = logging.getLogger(__name__)


def get_and_assert_urllib_response(request):
    response = urlopen(request)
    assert response.code == 200
    result = json.loads(response.read().decode('utf-8'))

    log.debug('urllib result:')
    log.debug(result)

    return result


@pytest.mark.parametrize(
    GET_DATA_PARAMS,
    GET_DATA.values(),
    ids=list(GET_DATA.keys()),
)
def test_urllib_get(httpbin, headers, params, extra):
    url = httpbin.url + '/get'
    if params:
        query = quote('&'.join('%s=%s' % (k, v) for k, v in params.items()))
        url = url + '?' + query

    request = Request(url=url, headers=headers)
    result = get_and_assert_urllib_response(request)
    assert_curl_response(UrllibRequest(request), extra, result)


@pytest.mark.parametrize(
    POST_DATA_PARAMS,
    POST_DATA.values(),
    ids=list(POST_DATA.keys()),
)
def test_urllib_post(httpbin, headers, data):
    url = httpbin.url + '/post'
    request = Request(url=url, headers=headers, data=data.encode('utf-8'))
    result = get_and_assert_urllib_response(request)
    assert_curl_response(UrllibRequest(request), object(), result)


@pytest.mark.parametrize(
    PROXY_DATA_PARAMS,
    PROXY_DATA.values(),
    ids=list(PROXY_DATA.keys()),
)
def test_urllib_proxy(httpbin, method, proxies, headers, data):
    run_proxy_server()
    url = httpbin.url + '/' + method

    request = Request(url=url, headers=headers)
    if data:
        request.data = data.encode('utf-8')

    http_proxy = proxies.get('http')
    os.environ['HTTP_PROXY'] = http_proxy
    result = get_and_assert_urllib_response(request)
    req = UrllibRequest(request)
    del os.environ['HTTP_PROXY']

    assert_curl_response(req, object(), result)
