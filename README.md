A cross-platform uptime for the Python. To install it, just do:

```
$ pip install uptime
```

Assuming you have [pip](http://www.pip-installer.org/) installed. If you don't, a tarball is [also available](http://pypi.python.org/pypi/uptime/).

Then just use it like this:

```python
from uptime import uptime

print uptime()
```

Full documentation [here](http://packages.python.org/uptime/). Works with any version of Python from 2.5 on, including Python 3.

Tested on Debian, FreeBSD, Windows XP, Mac OS X Lion, and OpenIndiana. Expected to work with every vaguely reasonable Linux and BSD, every Windows since Windows 2000, and Plan 9 From Bell Labs. Known *not* to work (yet) with Syllable or RISC OS. Patches welcome.
