#!/usr/bin/env python

import ctypes
import struct
import sys
import time

"""
Contains a bunch of functions that implement platform-specific ways to figure
out the system uptime, and one that uses all of them to figure out yours.
In principle, none of these functions create new processes or raise any
exceptions. They all return a float representing the number of seconds of
uptime, or None if they couldn't figure it out.
"""

def _uptime_linux():
    """Returns uptime in seconds or None, on Linux."""
    # With procfs
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])
    except (IOError, ValueError):
        pass

    # Without procfs (really?)
    try:
        libc = ctypes.CDLL('libc.so')
    except OSError:
        # Debian and derivatives do the wrong thing because /usr/lib/libc.so
        # is a GNU ld script rather than an ELF object. To get around this, we
        # have to be more specific.
        # We don't want to use ctypes.util.find_library because that creates a
        # new process on Linux. We also don't want to try too hard because at
        # this point we're already pretty sure this isn't Linux.
        try:
            libc = ctypes.CDLL('libc.so.6')
        except OSError:
            return None

    if not hasattr(libc, 'sysinfo'):
        # Not Linux
        return None

    buf = ctypes.create_string_buffer(128) # 64 suffices on 32-bit, whatever.
    if libc.sysinfo(buf) < 0:
        return None

    up = struct.unpack('@l', buf.raw[:struct.calcsize('@l')])[0]
    return up if up >= 0 else None

def _uptime_bsd():
    """Returns uptime in seconds or None, on BSD (including OS X)."""
    try:
        libc = ctypes.CDLL('libc.so')
    except OSError:
        # OS X; can't use ctypes.util.find_library because that creates
        # a new process on Linux, which is undesirable.
        try:
            libc = ctypes.CDLL('libc.dylib')
        except OSError:
            return None
    
    if not hasattr(libc, 'sysctlbyname'):
        # Not BSD
        return None

    # Determine how much space we need for the response
    sz = ctypes.c_uint(0)
    libc.sysctlbyname('kern.boottime', None, ctypes.byref(sz), None, 0)
    if sz.value != struct.calcsize('@LL'):
        # Unexpected, let's give up.
        return None

    # For real now
    buf = ctypes.create_string_buffer(sz.value)
    libc.sysctlbyname('kern.boottime', buf, ctypes.byref(sz), None, 0)
    sec, usec = struct.unpack('@LL', buf.raw)

    boottime = sec + usec / 1000000.
    up = time.time() - boottime
    return up if up > 0 else None

_uptime_osx = _uptime_bsd

def _uptime_plan9():
    """Returns uptime in seconds or None, on Plan 9."""
    # Apparently Plan 9 only has Python 2.2, which I'm not prepared to
    # support. Maybe some Linuxes implement /dev/time, though, someone was
    # taling about it somewhere.
    try:
        with open('/dev/time', 'r') as f:
            # The time file holds one 32-bit number representing the sec-
            # onds since start of epoch and three 64-bit numbers, repre-
            # senting nanoseconds since start of epoch, clock ticks, and
            # clock frequency.
            #  -- cons(3)
            s, ns, ct, cf = f.read().split()
            return float(ct) / float(cf)
    except (IOError, ValueError):
        return None

def _uptime_syllable():
    """Returns None, on Syllable."""
    return None

def _uptime_windows():
    """
    Returns uptime in seconds or None, on Windows. Warning: may return
    incorrect answers after 49.7 days on versions older than Vista.
    """
    if not hasattr(ctypes, 'windll') or not hasattr(ctypes.windll, 'kernel32'):
        return None
    if hasattr(ctypes.windll.kernel32, 'GetTickCount64'):
        # Vista/Server 2008 or later
        return ctypes.windll.kernel32.GetTickCount64() / 1000.
    if hasattr(ctypes.windll.kernel32, 'GetTickCount'):
        # Win2k or later; gives wrong answers after 49.7 days
        return ctypes.windll.kernel32.GetTickCount() / 1000.
    return None

def uptime():
    """Returns uptime in seconds if even remotely possible, or None if not."""
    if sys.platform == 'linux2':
        up = _uptime_linux()
        if up is not None:
            return up

    if sys.platform == 'win32':
        up = _uptime_windows()
        if up is not None:
            return up

    if sys.platform == 'darwin' or 'bsd' in sys.platform:
        up = _uptime_bsd()
        if up is not None:
            return up

    return _uptime_bsd() or _uptime_plan9() or \
           _uptime_linux() or _uptime_windows()


if __name__ == '__main__':
    up = uptime()
    if up is not None:
        h, m, s = up / 3600, up / 60 % 60, up % 60
        print 'Uptime: %02d:%02d:%02d (%.2f seconds).' % (h, m, s, up)
    else:
        print 'Unable to determine uptime. Patches welcome.'
