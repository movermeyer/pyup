#!/usr/bin/env python
"""PyUp - Markup generation tool.

:copyright: Copyright (c) 2015 by Robert Pogorzelski.
:license:   MIT, see LICENSE for more details.

"""
import sys

from setuptools.command.test import test as TestCommand
from setuptools import find_packages
from setuptools import setup


version = __import__('pyup').__version__


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='pyup',
    version=version,
    description='Markup generation tool',
    author='Robert Pogorzelski',
    author_email='thinkingpotato@gmail.com',
    url='http://github.com/thinkingpotato/pyup',
    license='MIT',
    platforms=['OS Independent'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Markup',
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
