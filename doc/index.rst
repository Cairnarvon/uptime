.. uptime documentation master file

:mod:`uptime` --- Cross-platform uptime library
===============================================

.. module:: uptime
   :synopsis: Cross-platform uptime library
.. moduleauthor:: Koen Crolla <cairnarvon@gmail.com>

This module provides a function—:func:`uptime.uptime`—that tells you how long
your system has been up. This turns out to be surprisingly non-straightforward,
but not impossible on any major platform. It tries to do this without creating
any child processes, because parsing ``uptime(1)``'s output is cheating.

It also exposes various platform-specific `helper functions`_, which you
probably won't need.

.. warning::

   On most platforms, this module depends very heavily on :mod:`ctypes`. It
   has become painfully apparent that many less mainstream platforms ship with
   a broken version of this standard library module, either accidentally or
   deliberately_. Please test your Python installation before using
   :mod:`uptime`.

.. _deliberately: https://developers.google.com/appengine/kb/libraries


Supported platforms
-------------------

These are the platforms on which :mod:`uptime` has been explicitly tested, and
the others on which it is therefore expected to work as well.

+------------------+--------+--------------------------+---------------------+
| Test platform    | Status | Function(s)              | Implications for... |
+==================+========+==========================+=====================+
| Android 4.0.3    | ✓      | :func:`_uptime_linux`    | Other versions of   |
|                  |        |                          | Android, hopefully  |
+------------------+--------+--------------------------+---------------------+
| Cygwin 1.7.17-1  | ✓      | :func:`_uptime_linux`    |                     |
+------------------+--------+--------------------------+---------------------+
| Debian Linux     | ✓      | :func:`_uptime_linux`,   | Every Linux since   |
| 6.0.6            |        | :func:`_uptime_posix`    | ~1994, Cygwin       |
+------------------+--------+--------------------------+---------------------+
| FreeBSD 9.1      | ✓      | :func:`_uptime_bsd`      | Every BSD           |
+------------------+--------+--------------------------+---------------------+
| Haiku R1 Alpha   | ✓      | :func:`_uptime_beos`     | BeOS                |
| 4.1              |        |                          |                     |
+------------------+--------+--------------------------+---------------------+
| Mac OS X "Lion"  | ✓      | :func:`_uptime_osx`      | Every Mac OS X      |
+------------------+--------+--------------------------+---------------------+
| OpenIndiana      | ✓      | :func:`_uptime_solaris`  | Solaris and its     |
| 151a7            |        |                          | free knock-offs     |
+------------------+--------+--------------------------+---------------------+
| Syllable Desktop | ✗ [*]_ | :func:`_uptime_syllable` | AtheOS              |
| 0.6.7            |        |                          |                     |
+------------------+--------+--------------------------+---------------------+
| Syllable Server  | ✓      | :func:`_uptime_linux`    |                     |
| 0.1              |        |                          |                     |
+------------------+--------+--------------------------+---------------------+
| Windows XP SP 3  | ✓      | :func:`_uptime_windows`  | Every Windows since |
|                  |        |                          | Windows 2000        |
+------------------+--------+--------------------------+---------------------+

.. [*] Not even the ``uptime(1)`` that ships with Syllable Desktop is able to
   determine the system uptime on that platform.

Additionally, :mod:`uptime` *should* work on Plan 9 From Bell Labs, but this
has not been tested. It probably won't work on any other operating systems not
listed, including AmigaOS and RISC OS.


The only function you should call
---------------------------------

.. function:: uptime

     >>> from uptime import uptime
     >>> uptime()
     49170.129999999997

   Returns the uptime in seconds, or :const:`None` if it can't figure it out.

   This function will try to call the right function for your platform (based
   on ``sys.platform``), or all functions in some order until it finds one
   that doesn't return :const:`None`.


Helper functions
----------------

All of these functions return either a floating point number representing the
number of seconds of uptime, or :const:`None`, same as :func:`uptime.uptime`.
You probably shouldn't call them yourself, but they're here if you want to.

Note that if :func:`uptime.uptime` returns :const:`None` for you, all of these
functions will return :const:`None` as well; they're really only good for
figuring out by which mechanism uptime was discovered.

.. function:: _uptime_beos

   BeOS/Haiku-specific uptime. It uses :c:func:`system_time` from ``libroot``
   to determine the uptime.

   .. versionadded:: 1.2

.. function:: _uptime_bsd

   BSD-specific uptime (including OS X). It uses ``sysctl`` (through the
   :c:func:`sysctlbyname` function) to figure out the system's boot time, which
   it then subtracts from the current time to find the uptime.

.. function:: _uptime_linux

   Linux-specific uptime. It first tries to read ``/proc/uptime``, and if that
   fails, it calls the :c:func:`sysinfo` C function.

.. function:: _uptime_osx

   Alias for :func:`_uptime_bsd`.

.. function:: _uptime_plan9

   Plan 9 From Bell Labs. Reads ``/dev/time``, which contains the number of
   clock ticks since boot and the number of clock ticks per seconds.

.. function:: _uptime_posix

   Fallback uptime for POSIX. Scans ``utmpx`` for a ``BOOT_TIME`` entry, and
   if it's present, subtracts its value from the current time to find the
   uptime.

   .. note::

      Because POSIX only specifies (some of) the members of
      :c:type:`struct utmpx` but not their order or exact sizes, nor the
      values of ``utmpx``'s constants (and there is no way to figure these
      things out at runtime), this is implemented as a C extension
      (:mod:`uptime._posix`) :mod:`distutils` tries to compile when you
      install :mod:`uptime`. If you're sure your ``utmpx`` database has a
      ``BOOT_TIME`` entry (many don't) but you're still getting :const:`None`
      for an answer, it may be the case that the extension couldn't be
      compiled.

   .. versionadded:: 1.3

.. function:: _uptime_solaris

   Solaris-specific uptime. This uses ``libkstat`` to find out the system's
   boot time (``unix:0:system_misc:boot_time``), which it then subtracts from
   the current time to find the uptime.

   .. versionadded:: 1.1

.. function:: _uptime_syllable

   Syllable-specific uptime. This does nothing at this point.

.. function:: _uptime_windows

   Windows-specific uptime. From Vista onward, it will call
   :c:func:`GetTickCount64` from Kernel32.lib. Before that (and since Windows
   2000), it calls :c:func:`GetTickCount`, which returns an unsigned 32-bit
   number representing the number of milliseconds since boot and will therefore
   overflow after 49.7 days. There is no way to tell when this has happened,
   but fortunately Windows systems won't stay up for that long.

   There is no solution yet for versions older than Windows 2000.

