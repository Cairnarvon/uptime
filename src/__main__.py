#!/usr/bin/env python

import sys
import time
from uptime import *

if __name__ == '__main__':
    up = uptime()
    boot = boottime()
    if up is not None:
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
        sys.stdout.write('Booted: %s.\n' % time.strftime('%c', boot))
    else:
        sys.stderr.write('Unable to determine uptime. Patches welcome.\n')
