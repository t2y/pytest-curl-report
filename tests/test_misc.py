# -*- coding: utf-8 -*-
import pytest

from requests.models import Response
from requests.models import Request as ReqRequest, PreparedRequest
from six.moves.urllib.request import Request

from pytest_curl_report import utils


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
