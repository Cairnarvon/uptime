#!/usr/bin/python

import os
import distutils.core
import distutils.ccompiler
import distutils.sysconfig

# This module has an optional extension component.
# If it doesn't build, it's not useful for your platform, but the pure-Python
# component still probably is. So, let's figure out what we can do.
try:
    compiler = distutils.ccompiler.new_compiler()
    compiler.add_include_dir(distutils.sysconfig.get_python_inc())
    distutils.sysconfig.customize_compiler(compiler)

    compiler.compile(['src/_posix.c'])

    # If we get here we succeeded. Hurray.
    ext = [distutils.core.Extension('uptime._posix', sources=['src/_posix.c'])]
    os.remove('src/_posix.o')
except:
    # Never mind.
    ext = None

distutils.core.setup(
    name='uptime',
    version='1.4.0',
    description='Cross-platform uptime library',
    long_description='''\
This module provides a cross-platform way to retrieve system uptime.
Supported platforms are Linux, Windows, OS X, *BSD, Solaris, Plan 9, and BeOS/Haiku.''',
    author='Koen Crolla',
    author_email='cairnarvon@gmail.com',
    url='https://github.com/Cairnarvon/uptime',
    package_dir={'uptime': 'src'},
    packages=['uptime'],
    ext_modules=ext,
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
