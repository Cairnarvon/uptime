Here's my to-do list, plus some avenues to explore to get there, in case
anyone else wants to have a go.


## AtheOS/Syllable Desktop

Syllable ships with the GNU coreutils, and its `uptime(1)` just doesn't work.
There also doesn't seem to be anything in, say, `/var/run` whose `mtime` or
`atime` we could use to determine boot time.

I've looked through the source code a few times, but found nothing of interest.

As a point of interest, [this page](http://atheos.syllable.org/uptime.php3.html)
seems to be broken. Maybe it's just not possible.


## DOS and Windows 3.x

I saw an old Pascal program (can't find the link now) that used
[`getftime`](http://www.delorie.com/djgpp/doc/libc/libc_394.html) on
[`NUL`](http://en.wikipedia.org/wiki/NUL:), but that gives the wrong answer on
(at least) Windows XP. If it really does work in real DOS (which I haven't
gotten around to testing), we need to check `_uptime_windows` first.

Apparently `GetTickCount` was already part of the Win16 API (where it returned
LONG instead of DWORD), so Windows 3.x support may be straightforward. It
probably has to be done as an extension, though, since `ctypes` is a bit too
modern.


## RISC OS

Unless someone gets a Python with `ctypes` working, we may have to write an
extension and include extensive manual build instructions. I don't imagine
`distutils` would cope very well.

I'm not even sure the current method would work with `ctypes`; `_swi` could be
a compiler extension and not part of `CLib`. RISC OS is so painful to work with
I haven't even checked.


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
