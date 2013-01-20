.. uptime documentation master file

Uptime: time for your ups
=========================

This module provides a function that tells you how long your system has been
up. This turns out to be surprisingly non-straightforward, but not impossible
on any major platform. It tries to do this without creating any child
processes, because parsing ``uptime(1)``'s output is cheating.

It also exposes various platform-specific helper functions, which you probably
won't need.

This module has been tested on Debian Linux, FreeBSD, NetBSD, Windows XP, and
Mac OS X Lion. It is expected to work on every vaguely reasonable version of
Linux and BSD, every version of Windows since Windows 2000, and Plan 9 From
Bell Labs. It is known *not* to work on Syllable and RISC OS (patches welcome).

The one you want
----------------

.. function:: uptime

     >>> from uptime import uptime
     >>> uptime()
     49170.129999999997

   Returns the uptime in seconds, or ``None`` if it can't figure it out.

   This function will try to call the right function for your platform (based
   on ``sys.platform``), or all functions in some order until it finds one
   that doesn't return ``None``.


Helper functions
----------------

All of these functions return either a floating point number representing the
number of seconds of uptime, or ``None``, same as :func:`uptime`. You probably
shouldn't call them yourself, but they're here if you want to.

.. function:: _uptime_bsd

   BSD-specific uptime (including OS X). It uses ``sysctl`` (though the
   ``sysctlbyname(3)`` function) to figure out the system's boot time, which
   it then subtracts from the current time to find the uptime.

.. function:: _uptime_linux

   Linux-specific uptime. It first tries to read ``/proc/uptime``, and if that
   fails, it calls the ``sysinfo(2)`` C function.

.. function:: _uptime_osx

   Alias for :func:`_uptime_bsd`.

.. function:: _uptime_plan9

   Plan 9 From Bell Labs. Reads ``/dev/time``, which contains the number of
   clock tics since boot and the number of clock ticks per seconds.

.. function:: _uptime_syllable

   Syllable-specific uptime. This does nothing at this point.

.. function:: _uptime_windows

   Windows-specific uptime. From Vista onward, it will call ``GetTickCount64``
   from Kernel32.lib. Before that (and since Windows 2000), it calls
   ``GetTickCount``, which returns an unsigned 32-bit number representing the
   number of milliseconds since boot and will therefore overflow after 49.7
   days. There is no way to tell when this has happened, but fortunately
   Windows systems won't stay up for that long.

   There is no solution yet for versions older than Windows 2000.

