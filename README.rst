.. image:: https://drone.io/bitbucket.org/pytest-dev/pytest-curl-report/status.png
   :target: https://drone.io/bitbucket.org/pytest-dev/pytest-curl-report/latest
.. image:: https://pypip.in/v/pytest-curl-report/badge.png
   :target: https://pypi.python.org/pypi/pytest-curl-report

Requirements
------------

* Python 2.6 or 3.3 and later


Features
--------

* Provide additional `cURL`_ report if a testcase includes http request would fail
* Support urllib/urllib2 and `requests`_ as a http request object
* Support cURL command line below options

  * method
  * proxy
  * header
  * form data
  * attachment file

.. _cURL: http://curl.haxx.se/
.. _requests: http://docs.python-requests.org/


Installation
============

::

    $ pip install pytest-curl-report


Quick Start
===========

Create a test file requesting a web server via http[s] and intend to fail
the test.

::

    $ vi test.py
    # -*- coding: utf-8 -*-
    import requests

    def test_requests_get():
        r = requests.get('http://httpbin.org/get')
        assert False

Then, pytest shows the report as below.

::

    $ py.test test.py
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.9 -- py-1.4.27 -- pytest-2.6.4
    plugins: curl-report, httpbin, cache, capturelog, cov, flakes, pep8
    collected 1 items 

    test.py F

    =================================== FAILURES ===================================
    ______________________________ test_requests_get _______________________________

        def test_requests_get():
            r = requests.get('http://httpbin.org/get')
    >       assert False
    E       assert False

    test.py:7: AssertionError
    -------------------------- How to reproduce with curl --------------------------
    curl -X GET -H "Connection: keep-alive" -H "Accept-Encoding: gzip, deflate"
    -H "Accept: */*" -H "User-Agent: python-requests/2.7.0 CPython/2.7.9 Darwin/14.3.0"
    "http://httpbin.org/get"

The pytest-curl-report plugin generates cURL command line to reproduce http
request to the web server. Copy the cURL command and paste it on terminal,
then you can run the command immediately. It might be useful to tell the
developers how to reproduce an issue when the test was failed.

The cURL report would be generated from *Request* object in test code,
so you don't have to configure some settings or use particular snippet.


Usage
=====

There are several options.

::

    $ py.test -h
    ...
    curl report:
      --no-curl-report      not generate curl report when a testcase is failed
      --curl-report-only    strip pytest assertion log and generate curl report
                            only
    ...

*--curl-report-only* is useful if you want to confirm cURL commands only.
For example, you prefer test first concept and use the cli for interactive
development.

::

    $ vi test.py
    ...
    def test_requests_post():
        r = requests.post('https://httpbin.org/post', data={"test": "example"})
        assert False

    $ py.test --curl-report-only test.py 
    =================================== FAILURES ===================================
    ______________________________ test_requests_get _______________________________
    -------------------------- How to reproduce with curl --------------------------
    curl -X GET -H "Connection: keep-alive" -H "Accept-Encoding: gzip, deflate"
    -H "Accept: */*" -H "User-Agent: python-requests/2.7.0 CPython/2.7.9 Darwin/14.3.0"
    "http://httpbin.org/get"
    ______________________________ test_requests_post ______________________________
    -------------------------- How to reproduce with curl --------------------------
    curl -X POST -H "Content-Length: 12" -H "Accept-Encoding: gzip, deflate"
    -H "Accept: */*" -H "User-Agent: python-requests/2.7.0 CPython/2.7.9 Darwin/14.3.0"
    -H "Connection: keep-alive" -H "Content-Type: application/x-www-form-urlencoded"
    -d "test=example" "https://httpbin.org/post"
    =========================== 2 failed in 1.33 seconds ===========================

As described above, you might think that some headers are redundant.
Add some code into conftest.py, then restrict headers you need.

::

    $ vi conftest.py
    def pytest_namespace():
        return {'curl_report': {'headers': ['Content-Type']}}

    $ py.test test.py
    ...
    ______________________________ test_requests_post ______________________________
    -------------------------- How to reproduce with curl --------------------------
    curl -X POST -H "Content-Type: application/x-www-form-urlencoded"
    -d "test=example" "https://httpbin.org/post"

In this case, only *Content-Type* header is generated.

Proxy Settings
--------------

Unfortunately, it seems *Request* object doesn't keep proxy settings.
Proxy settings are retrieved from environment variable on platform.
So add environment variable to detect the settings by plugin,
even if you give the settings with another way.

::

    $ vi test.py
    def test_requests_proxy_post():
        import os
        os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:8888'
        r = requests.post('https://httpbin.org/post', data={"test": "example"})
        assert False

    $ py.test test.py
    ...
    -------------------------- How to reproduce with curl --------------------------
    curl -X POST -x https://127.0.0.1:8888
    -H "Content-Type: application/x-www-form-urlencoded" -d "test=example"
    "https://httpbin.org/post"

