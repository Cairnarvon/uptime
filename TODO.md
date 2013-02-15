Here's my to-do list, plus some avenues to explore to get there, in case
anyone else wants to have a go.


## DOS and Windows 3.x

I found [an old Pascal program](http://www.freedos.org/software/?prog=uptime)
that uses [`getftime`](http://www.delorie.com/djgpp/doc/libc/libc_394.html) on
[`NUL`](http://en.wikipedia.org/wiki/NUL:), but that gives the wrong answer on
FreeDOS (and, for that matter, Windows XP), so it isn't usable.

Apparently `GetTickCount` was already part of the Win16 API (where it returned
LONG instead of DWORD), so Windows 3.x support may be straightforward. It
probably has to be done as an extension, though, since `ctypes` is a bit too
modern.


## Palm OS

There are several Palm OS ports of Python, but they all seem to be 1.5.x, which
I'm not supporting. In case a more recent version comes along, though, here's
some information:

```c
#include <TimeMgr.h>
#include <SystemMgr.h>

double _uptime_palmos(void)
{
    return TimeGetTicks() / SysTicksPerSecond();
}
```

The tick count doesn't advance while the system is in sleep mode. I'm not
sure if that's something that bothers me, but it does have implications for
the calculation of boot time.

Since `TimeGetTicks` returns a `UInt32`, this will wrap around in 136 years
at best, and (as `SysTicksPerSecond` returns a `UInt16`) slightly over 18 hours
at worst.

There's almost certainly a way to get at the time of the last reset directly
(there's an [uptime app](http://normsoft.com/products/palm/uptime/) that shows
the time of the first reset, last reset, and number of resets), but the Palm OS
[API reference](http://dogbert.mse.cs.cmu.edu/charlatans/References/Tech_Doc/Palm%20OS%205.0%20Docs/Palm%20OS%20Reference.pdf)
is 2426 pages. I'll find it eventually.


## Symbian

```cpp
#include <hal.h>

double _uptime_symbian(void)
{
    TInt tickspersecond;

    HAL::Get(HALData::ESystemTickPeriod, tickspersecond);
    return (double)User::TickCount() / tickspersecond;
}
```

This is Sepples, so `ctypes` can't deal with it. I have no idea how feasible
building Sepples extensions on/for Symbian is, but I doubt it's painless. I've
gotten as far as registering a Nokia developer account and downloading the SDK.


## Windows CE

This really just needs testing. I'm told PythonCE has a working `ctypes`, so I
don't expect a huge amount of trouble. I just don't have a Windows CE image
capable of running PythonCE at this point, and building one requires a whole
mess of Microsoft unpleasantry. I'll get around to it.
