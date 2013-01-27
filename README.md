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

Or run the module as a script:

```
$ python -m uptime
Uptime: 109 days, 33.84 seconds.
```

(You may need to use `uptime.__main__`, depending on your version of Python.)

Full documentation [here](http://packages.python.org/uptime/). Works with any version of Python from 2.5 on, including Python 3.

Tested on Debian, FreeBSD, Windows XP, Mac OS X Lion, OpenIndiana, and Haiku. Expected to work with every vaguely reasonable Linux and BSD, every Windows since Windows 2000, and Plan 9 From Bell Labs.

### TODO

+ AtheOS/Syllable
+ MS-DOS and earlier versions of Windows
+ RISC OS
+ Windows CE

Know any other platforms I should add? [Let me know.](https://github.com/Cairnarvon/uptime/issues)
