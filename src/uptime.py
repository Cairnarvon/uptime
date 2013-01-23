#!/usr/bin/env python

"""
Provides a cross-platform way to figure out the system uptime.

Should work on damned near any operating system you can realistically expect
to be asked to write Python code for.
If this module is invoked as a stand-alone script, it will print the current
uptime in a human-readable format, or display an error message if it can't,
to standard output.

"""

import ctypes
import struct
import sys
import time

def _uptime_linux():
    """Returns uptime in seconds or None, on Linux."""
    # With procfs
    try:
        f = open('/proc/uptime', 'r')
        up = float(f.readline().split()[0])
        f.close()
        return up
    except (IOError, ValueError):
        pass

    # Without procfs (really?)
    try:
        libc = ctypes.CDLL('libc.so')
    except (OSError, RuntimeError):
        # Debian and derivatives do the wrong thing because /usr/lib/libc.so
        # is a GNU ld script rather than an ELF object. To get around this, we
        # have to be more specific.
        # We don't want to use ctypes.util.find_library because that creates a
        # new process on Linux. We also don't want to try too hard because at
        # this point we're already pretty sure this isn't Linux.
        try:
            libc = ctypes.CDLL('libc.so.6')
        except (OSError, RuntimeError):
            return None

    if not hasattr(libc, 'sysinfo'):
        # Not Linux.
        return None

    buf = ctypes.create_string_buffer(128) # 64 suffices on 32-bit, whatever.
    if libc.sysinfo(buf) < 0:
        return None

    up = struct.unpack('@l', buf.raw[:struct.calcsize('@l')])[0]
    return up if up >= 0 else None

def _uptime_beos():
    """Returns uptime in seconds on None, on BeOS/Haiku."""
    try:
        libroot = ctypes.CDLL('libroot.so')
    except (OSError, RuntimeError):
        return None

    libroot.system_time.restype = ctypes.c_int64
    return libroot.system_time() / 1000000.

def _uptime_bsd():
    """Returns uptime in seconds or None, on BSD (including OS X)."""
    try:
        libc = ctypes.CDLL('libc.so')
    except (OSError, RuntimeError):
        # OS X; can't use ctypes.util.find_library because that creates
        # a new process on Linux, which is undesirable.
        try:
            libc = ctypes.CDLL('libc.dylib')
        except (OSError, RuntimeError):
            return None
    
    if not hasattr(libc, 'sysctlbyname'):
        # Not BSD.
        return None

    # Determine how much space we need for the response.
    sz = ctypes.c_uint(0)
    libc.sysctlbyname('kern.boottime', None, ctypes.byref(sz), None, 0)
    if sz.value != struct.calcsize('@LL'):
        # Unexpected, let's give up.
        return None

    # For real now.
    buf = ctypes.create_string_buffer(sz.value)
    libc.sysctlbyname('kern.boottime', buf, ctypes.byref(sz), None, 0)
    sec, usec = struct.unpack('@LL', buf.raw)

    # OS X disagrees what that second value is.
    if usec > 1000000:
        usec = 0.

    boottime = sec + usec / 1000000.
    up = time.time() - boottime
    return up if up > 0 else None

_uptime_osx = _uptime_bsd

def _uptime_plan9():
    """Returns uptime in seconds or None, on Plan 9."""
    # Apparently Plan 9 only has Python 2.2, which I'm not prepared to
    # support. Maybe some Linuxes implement /dev/time, though, someone was
    # talking about it somewhere.
    try:
        # The time file holds one 32-bit number representing the sec-
        # onds since start of epoch and three 64-bit numbers, repre-
        # senting nanoseconds since start of epoch, clock ticks, and
        # clock frequency.
        #  -- cons(3)
        f = open('/dev/time', 'r')
        s, ns, ct, cf = f.read().split()
        f.close()
        return float(ct) / float(cf)
    except (IOError, ValueError):
        return None

def _uptime_solaris():
    """Returns uptime in seconds or None, on Solaris."""
    try:
        kstat = ctypes.CDLL('libkstat.so')
    except (OSError, RuntimeError):
        return None

    # kstat doesn't have uptime, but it does have boot time.
    boottime = None

    # Unfortunately, getting at it isn't perfectly straightforward.
    # First, let's pretend to be kstat.h

    # Constant
    KSTAT_STRLEN = 31   # According to every kstat.h I could find.

    # Data structures
    class anon_union(ctypes.Union):
        # The ``value'' union in kstat_named_t actually has a bunch more
        # members, but we're only using it for boot_time, so we only need
        # the padding and the one we're actually using.
        _fields_ = [('c', ctypes.c_char * 16),
                    ('time', ctypes.c_int)]

    class kstat_named_t(ctypes.Structure):
        _fields_ = [('name', ctypes.c_char * KSTAT_STRLEN),
                    ('data_type', ctypes.c_char),
                    ('value', anon_union)]

    # Function signatures
    kstat.kstat_open.restype = ctypes.c_void_p
    kstat.kstat_lookup.restype = ctypes.c_void_p
    kstat.kstat_lookup.argtypes = [ctypes.c_void_p,
                                   ctypes.c_char_p,
                                   ctypes.c_int,
                                   ctypes.c_char_p]
    kstat.kstat_read.restype = ctypes.c_int
    kstat.kstat_read.argtypes = [ctypes.c_void_p,
                                 ctypes.c_void_p,
                                 ctypes.c_void_p]
    kstat.kstat_data_lookup.restype = ctypes.POINTER(kstat_named_t)
    kstat.kstat_data_lookup.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p]

    # Now, let's do something useful.

    # Initialise kstat control structure.
    kc = kstat.kstat_open()
    if not kc:
        return None

    # We're looking for unix:0:system_misc:boot_time.
    ksp = kstat.kstat_lookup(kc, 'unix', 0, 'system_misc')
    if ksp and kstat.kstat_read(kc, ksp, None) != -1:
        data = kstat.kstat_data_lookup(ksp, 'boot_time')
        if data:
            boottime = data.contents.value.time

    # Clean-up.
    kstat.kstat_close(kc)

    if boottime is not None:
        return time.time() - boottime

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
        # Vista/Server 2008 or later.
        return ctypes.windll.kernel32.GetTickCount64() / 1000.
    if hasattr(ctypes.windll.kernel32, 'GetTickCount'):
        # Win2k or later; gives wrong answers after 49.7 days.
        return ctypes.windll.kernel32.GetTickCount() / 1000.
    return None

def uptime():
    """Returns uptime in seconds if even remotely possible, or None if not."""
    return {'beos5': _uptime_beos,
            'cygwin': _uptime_linux,
            'darwin': _uptime_osx,
            'haiku1': _uptime_beos,
            'linux2': _uptime_linux,
            'sunos5': _uptime_solaris,
            'win32': _uptime_windows}.get(sys.platform, _uptime_bsd)() or \
           _uptime_bsd() or _uptime_plan9() or _uptime_linux() or \
           _uptime_windows() or _uptime_solaris() or _uptime_beos()


if __name__ == '__main__':
    up = uptime()
    if up is not None:
        h, m, s = up / 3600, up / 60 % 60, up % 60
        sys.stdout.write('Uptime: %02d:%02d:%02d (%.2f seconds).\n' % (h, m, s, up))
    else:
        sys.stdout.write('Unable to determine uptime. Patches welcome.\n')
