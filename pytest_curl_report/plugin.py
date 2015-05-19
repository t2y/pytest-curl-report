# -*- coding: utf-8 -*-
import pytest

from .curl import Curl
from .utils import get_inspect_functions


PLUGIN_NAMESPACE = 'curl_report'


def pytest_addoption(parser):
    group = parser.getgroup('curlreport', 'curl report')
    group.addoption(
        '--no-curl-report', dest='no_curl_report',
        action='store_true', default=False,
        help='not generate curl report when a testcase is failed'
    )
    group.addoption(
        '--curl-report-only', dest='curl_report_only',
        action='store_true', default=False,
        help='strip pytest assertion log and generate curl report only'
    )


def pytest_runtest_makereport(__multicall__, item, call):
    if item.config.option.no_curl_report:
        return

    report = __multicall__.execute()
    if report.longrepr is None:
        return report

    if item.config.option.curl_report_only:
        if hasattr(report, 'longrepr'):
            if hasattr(report.longrepr, 'reprtraceback'):
                # HACK: set dummy reporting function for traceback report
                report.longrepr.reprtraceback.toterminal = lambda x: None

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
