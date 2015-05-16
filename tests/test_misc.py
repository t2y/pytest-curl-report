# -*- coding: utf-8 -*-
import pytest

from requests.models import Response
from requests.models import Request as ReqRequest, PreparedRequest
from six.moves.urllib.request import Request

from pytest_curl_report import curl
from pytest_curl_report import utils


@pytest.mark.parametrize(('data', 'content_type', 'expected'), [
    (
        '--bbbcurlreportbbb\r\n'
        'Content-Disposition: form-data; name="data1"\r\n\r\n'
        'test1\r\n'
        '--bbbcurlreportbbb\r\n'
        'Content-Disposition: form-data; name="data2"\r\n\r\n'
        'test2\r\n',
        'multipart/form-data; boundary=bbbcurlreportbbb',
        {'data1': ['test1'], 'data2': ['test2']},
    ),
    (
        '--bbbcurlreportbbb\r\n'
        'Content-Disposition: form-data; name="data1"\r\n\r\n'
        'test1\r\n'
        '--bbbcurlreportbbb\r\n'
        'Content-Disposition: form-data; name="data1"\r\n\r\n'
        'test2\r\n',
        'multipart/form-data; boundary=bbbcurlreportbbb',
        {'data1': ['test1', 'test2']},
    ),
], ids=[
    'with basic multipart/form-data',
    'with multipart/form-data to send multiple data',
])
def test_parse_multipart_formdata(data, content_type, expected):
    encoded = data.encode('utf-8')
    formdata, _ = curl.parse_multipart_data(encoded, content_type)
    for key, values in formdata.items():
        formdata[key] = [value.decode('utf-8') for value in values]
    assert formdata == expected


def test_get_inspect_functions():
    funcs = utils.get_inspect_functions()
    assert len(funcs) == 2


@pytest.mark.parametrize(('obj', 'expected'), [
    (Request('http://localhost'), utils.UrllibRequest),
    (object(), None),
], ids=[
    'urllib.Request',
    'object',
])
def test_get_urllib_request(obj, expected):
    assert_get_request_object(utils.get_urllib_request, obj, expected)


def test_has_requests():
    assert utils.has_requests() is True


_REQUESTS_RESPONSE = Response()
_REQUESTS_RESPONSE.request = PreparedRequest()


@pytest.mark.parametrize(('obj', 'expected'), [
    (_REQUESTS_RESPONSE, utils.RequestsRequest),
    (ReqRequest(), utils.RequestsRequest),
    (PreparedRequest(), utils.RequestsRequest),
    (object(), None),
], ids=[
    'requests.Response',
    'requests.Request',
    'requests.PreparedRequest',
    'object',
])
def test_get_requests_request(obj, expected):
    assert_get_request_object(utils.get_requests_request, obj, expected)


def assert_get_request_object(func, obj, expected):
    actual = func(obj)
    if expected is None:
        assert actual is None
    else:
        assert isinstance(actual, expected)
