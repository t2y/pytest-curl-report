# -*- coding: utf-8 -*-
import pytest

from .utils import Curl
from .utils import get_inspect_functions


PLUGIN_NAMESPACE = 'curl_report'


def pytest_addoption(parser):
    parser.addoption(
        '--no-curl-report', dest='nocurlreport',
        action='store_true', default=False,
        help='not generate curl report when a testcase is failed'
    )


def pytest_runtest_makereport(__multicall__, item, call):
    if item.config.option.nocurlreport:
        return

    report = __multicall__.execute()
    if not report.longrepr:
        return report

    extra_info = getattr(pytest, PLUGIN_NAMESPACE, object())
    inspect_funcs = get_inspect_functions()
    for _, obj in call.excinfo.traceback[0].frame.f_locals.items():
        for func in inspect_funcs:
            r = func(obj)
            if r is not None:
                cmd = Curl(r, extra_info).make_command()
                report.longrepr.addsection('How to reproduce with curl', cmd)
                break

    return report
