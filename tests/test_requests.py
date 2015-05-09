# -*- coding: utf-8 -*-
import json
import logging

import pytest
import requests

from pytest_curl_report.utils import RequestsRequest

from data import GET_DATA, GET_DATA_PARAMS
from data import POST_DATA, POST_DATA_PARAMS
from utils import assert_curl_response

log = logging.getLogger(__name__)


@pytest.mark.parametrize(
    GET_DATA_PARAMS,
    GET_DATA.values(),
    ids=list(GET_DATA.keys()),
)
def test_requets_get(httpbin, headers, params, extra):
    url = httpbin.url + '/get'
    r = requests.get(url, headers=headers, params=params)
    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.get result:')
    log.debug(result)

    assert_curl_response(RequestsRequest(r.request), extra, result)


@pytest.mark.parametrize(
    POST_DATA_PARAMS,
    POST_DATA.values(),
    ids=list(POST_DATA.keys()),
)
def test_requests_post(httpbin, headers, data):
    url = httpbin.url + '/post'
    r = requests.post(url, headers=headers, data=data)
    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.post result:')
    log.debug(result)

    assert_curl_response(RequestsRequest(r.request), object(), result)
