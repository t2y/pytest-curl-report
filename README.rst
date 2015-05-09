.. image:: https://drone.io/bitbucket.org/pytest-dev/pytest-curl-report/status.png
   :target: https://drone.io/bitbucket.org/pytest-dev/pytest-curl-report/latest
.. image:: https://pypip.in/v/pytest-curl-report/badge.png
   :target: https://pypi.python.org/pypi/pytest-curl-report

Requirements
------------

* Python 2.6 or 3.3 and later

Features
--------

* Provide additional cURL report if http request included in a testcase
  would fail

Installation
============

::

    $ pip install pytest-curl-report

Quick Start
===========


Usage
=====

conftest.py

::

    def pytest_namespace():
        return {'curl_report': {'headers': ['Content-Type', 'User-Agent']}}

