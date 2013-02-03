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
Booted: Wed Oct 10 06:28:24 2012.
```

(You may need to use `uptime.__main__`, depending on your version of Python.)

Full documentation [here](http://packages.python.org/uptime/). Works with any version of Python from 2.5 on, including Python 3.

Tested on a bunch of platforms, expected to work on a bunch more. See the documentation for details.

For a list of platforms I'm working on adding, see [here](TODO.md). Know any others I should add? [Let me know.](https://github.com/Cairnarvon/uptime/issues)
