#!/usr/bin/python

import sys
import distutils.core
import distutils.ccompiler
import distutils.sysconfig

# This package has optional extension components. If they can't build, odds
# are it's not a big deal, but there doesn't seem to be a convenient way to
# tell distutils this. So let's just try compiling them and keeping track of
# those that work.
sys.stdout.write('Trial compilation of extensions. Ignore any errors.\n')
ext = []
for module in ('_posix',):
    try:
        compiler = distutils.ccompiler.new_compiler()
        compiler.add_include_dir(distutils.sysconfig.get_python_inc())
        distutils.sysconfig.customize_compiler(compiler)
        compiler.compile(['src/%s.c' % module])
    except:
        pass
    else:
        ext.append(distutils.core.Extension('uptime.%s' % module,
                                            sources=['src/%s.c' % module]))
sys.stdout.write('End of trial compilation. Will build %s.\n' %
                 (', '.join(e.name for e in ext) or 'none'))

distutils.core.setup(
    name='uptime',
    version='2.0.0',
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
