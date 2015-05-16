# -*- coding: utf-8 -*-
import json
import os
import logging
from os.path import basename

import pytest
import requests

from pytest_curl_report.utils import RequestsRequest

from data import GET_DATA, GET_DATA_PARAMS
from data import POST_DATA, POST_DATA_PARAMS
from data import POST_DATA_MULTIPART, POST_DATA_MULTIPART_PARAMS
from data import PUT_DATA, PUT_DATA_PARAMS
from data import DELETE_DATA, DELETE_DATA_PARAMS
from data import PROXY_DATA, PROXY_DATA_PARAMS
from utils import assert_curl_response, run_proxy_server

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


@pytest.mark.parametrize(
    POST_DATA_MULTIPART_PARAMS,
    POST_DATA_MULTIPART.values(),
    ids=list(POST_DATA_MULTIPART.keys()),
)
def test_requests_multipart_post(httpbin, headers, data):
    # for some reason, requests would not handle arbitrary content-type
    # in multipart/form-data, so remove, but requests would add it
    headers = headers.copy()
    headers.pop('Content-Type')

    attachment_paths = []
    data = data.copy()
    for key, values in data.items():
        if values[0] is not None:
            attachment_paths.append(values[1])
            data[key] = (values[0], open(values[1]))

    if attachment_paths:
        log.debug('attachment files:')
        log.debug(attachment_paths)

    url = httpbin.url + '/post'
    r = requests.post(url, headers=headers, files=data)
    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.post with multipart result:')
    log.debug(result)

    # setup
    for path in attachment_paths:
        fname = basename(path)
        if not os.access(fname, os.F_OK):
            os.symlink(path, fname)

    assert_curl_response(RequestsRequest(r.request), object(), result)

    # tear down
    for path in attachment_paths:
        if os.access(fname, os.F_OK):
            os.remove(basename(path))


@pytest.mark.parametrize(
    PUT_DATA_PARAMS,
    PUT_DATA.values(),
    ids=list(PUT_DATA.keys()),
)
def test_requests_put(httpbin, headers, data):
    url = httpbin.url + '/put'
    r = requests.put(url, headers=headers, data=data)
    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.put result:')
    log.debug(result)

    assert_curl_response(RequestsRequest(r.request), object(), result)


@pytest.mark.parametrize(
    DELETE_DATA_PARAMS,
    DELETE_DATA.values(),
    ids=list(PUT_DATA.keys()),
)
def test_requests_delete(httpbin, headers, data):
    url = httpbin.url + '/delete'
    r = requests.delete(url, headers=headers, data=data)
    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.delete result:')
    log.debug(result)

    assert_curl_response(RequestsRequest(r.request), object(), result)


@pytest.mark.parametrize(
    PROXY_DATA_PARAMS,
    PROXY_DATA.values(),
    ids=list(PROXY_DATA.keys()),
)
def test_requests_http_proxy(httpbin, method, proxies, headers, data):
    run_proxy_server()
    url = httpbin.url + '/' + method

    http_proxy = proxies.get('http')
    os.environ['HTTP_PROXY'] = http_proxy
    r = requests.request(method, url, headers=headers, data=data)
    req = RequestsRequest(r.request)
    del os.environ['HTTP_PROXY']

    assert r.status_code == 200
    result = json.loads(r.content.decode('utf-8'))

    log.debug('requets.%s via %s result:' % (method, http_proxy))
    log.debug(result)

    assert_curl_response(req, object(), result)
