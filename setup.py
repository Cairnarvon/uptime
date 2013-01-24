#!/usr/bin/python

from distutils.core import setup

setup(
    name='uptime',
    version='1.2.1',
    description='Cross-platform uptime library',
    long_description='''\
This module provides a cross-platform way to retrieve system uptime.
Supported platforms are Linux, Windows, OS X, *BSD, Solaris, Plan 9, and BeOS/Haiku.''',
    author='Koen Crolla',
    author_email='cairnarvon@gmail.com',
    url='https://github.com/Cairnarvon/uptime',
    package_dir={'': 'src'},
    py_modules=['uptime'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: System Administrators',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: BSD',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: POSIX :: Other',
                 'Operating System :: POSIX :: SunOS/Solaris',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: System']
)
