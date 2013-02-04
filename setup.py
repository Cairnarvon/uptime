#!/usr/bin/python

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils import log

class ve_build_ext(build_ext):
    # The uptime package has (an) optional extension component(s).
    # If they don't build, they probably don't apply to your platform and
    # should be ignored. If they do apply, they can probably still be ignored
    # anyway.
    def run(self):
        try:
            build_ext.run(self)
        except:
            log.warn('not building extensions')

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except:
            log.warn('build failed: %s (no big deal)' % ext.name)

dist = setup(
    name='uptime',
    version='2.0.1',
    description='Cross-platform uptime library',
    long_description='''\
This module provides a cross-platform way to retrieve system uptime.
Supported platforms are Linux, Windows, OS X, *BSD, Solaris, Plan 9, and BeOS/Haiku.''',
    author='Koen Crolla',
    author_email='cairnarvon@gmail.com',
    url='https://github.com/Cairnarvon/uptime',
    cmdclass={'build_ext': ve_build_ext},
    package_dir={'uptime': 'src'},
    packages=['uptime'],
    ext_modules=[Extension('uptime._posix', sources=['src/_posix.c'])],
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
