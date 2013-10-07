#!/usr/bin/env python

import sys
import time
from uptime import *

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

if __name__ == '__main__':
    up = uptime()

    if up is None:
        sys.stderr.write('Unable to determine uptime. Patches welcome.\n')
        sys.exit(1)

    if '-b' not in sys.argv:
        parts = []

        days, up = up // 86400, up % 86400
        if days:
            parts.append('%d day%s' % (days, 's' if days != 1 else ''))

        hours, up = up // 3600, up % 3600
        if hours:
            parts.append('%d hour%s' % (hours, 's' if hours != 1 else ''))

        minutes, up = up // 60, up % 60
        if minutes:
            parts.append('%d minute%s' % (minutes, 's' if minutes != 1 else ''))

        if up or not parts:
            parts.append('%.2f seconds' % up)

        sys.stdout.write('Uptime: %s.\n' % ', '.join(parts))
    else:
        sys.stdout.write(boottime().strftime('Booted: %c.\n'))
