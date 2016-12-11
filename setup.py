# -*- coding: utf-8 -*-
import re

from setuptools import setup


try:
    LONG_DESCRIPTION = ''.join([
        open('README.rst').read(),
        open('CHANGELOG.rst').read(),
    ])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

init_py = open('pytest_curl_report/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))


setup(
    name='pytest-curl-report',
    version=metadata['version'],
    description='pytest plugin to generate curl command line report',
    license='Apache License 2.0',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Quality Assurance',
    ],
    keywords=['test', 'pytest', 'curl'],
    author='Tetsuya Morimoto',
    author_email='tetsuya.morimoto@gmail.com',
    url='https://bitbucket.org/pytest-dev/pytest-curl-report',
    platforms=['linux', 'osx', 'unix', 'win32'],
    packages=['pytest_curl_report'],
    entry_points={'pytest11': ['curl-report = pytest_curl_report.plugin']},
    install_requires=['pytest>=2.4'],
    tests_require=[
        'pyproxy',
        'pytest',
        'pytest-capturelog',
        'pytest-cov',
        'pytest-flakes',
        'pytest-httpbin',
        'pytest-pep8',
        'requests',
        'six',
        'tox',
    ],
)
