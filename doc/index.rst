.. uptime documentation master file

:mod:`uptime` --- Cross-platform uptime library
===============================================

.. module:: uptime
   :synopsis: Cross-platform uptime library
.. moduleauthor:: Koen Crolla <cairnarvon@gmail.com>

This module provides a function that tells you how long your system has been
up. This turns out to be surprisingly non-straightforward, but not impossible
on any major platform. It tries to do this without creating any child
processes, because parsing ``uptime(1)``'s output is cheating.

It also exposes various platform-specific helper functions, which you probably
won't need.

This module has been tested on Debian Linux, FreeBSD, Windows XP, Mac OS X
Lion, OpenIndiana, and Haiku. It is additionally expected to work on every
vaguely reasonable version of Linux and BSD, every version of Windows since
Windows 2000, and Plan 9 From Bell Labs. It is known *not* to work on Syllable
and RISC OS (patches welcome).

.. warning::

   This module depends very heavily on :mod:`ctypes`. It has become painfully
   apparent that many less mainstream platforms ship with a broken version of
   this standard library module, either accidentally or deliberately_. Please
   test your Python installation before using :mod:`uptime`.

.. _deliberately: https://developers.google.com/appengine/kb/libraries

The one you want
----------------

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

.. function:: _uptime_beos

   BeOS/Haiku-specific uptime. It uses :c:func:`system_time` from ``libroot``
   to determine the uptime.

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

.. function:: _uptime_solaris

   Solaris-specific uptime. This uses ``libkstat`` to find out the system's
   boot time (``unix:0:system_misc:boot_time``), which it then subtracts from
   the current time to find the uptime.

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

