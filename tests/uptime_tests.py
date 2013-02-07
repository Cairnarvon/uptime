#!/usr/bin/env python
# coding: utf8

import imp
import sys
import time
import unittest

sys.path.insert(0, '.')

import src as uptime


boottime_helpers = [f for f in vars(uptime) if f.startswith('_boottime_')]
uptime_helpers = [f for f in vars(uptime) if f.startswith('_uptime_')]


class NormalTest(unittest.TestCase):
    """
    This class just calls each of the functions normally and ensures they don't
    do dumb things like throw exceptions or return complex numbers.
    """
    def tearDown(self):
        """
        __boottime affects how boottime() and its helpers work, and it may be
        set as a side-effect by any function. To be on the safe side, just
        reload the whole module every time.
        """
        imp.reload(uptime)

    def basic_test(self, func, rettype):
        """
        Calls a given function and checks if it returns None or something of
        type rettype.
        """
        ret = func()
        self.assertTrue(ret is None or isinstance(ret, rettype))

    def __getattr__(self, name):
        # I really don't feel like writing and maintaining over a dozen
        # essentially identical methods, and if there's a cleaner way to do
        # this, I couldn't find it in the unittest docs.
        if name.startswith('test_'):
            func = name[5:]
            if func == 'uptime' or func in uptime_helpers:
                rettype = float
            elif func == 'boottime' or func in boottime_helpers:
                rettype = time.struct_time
            else:
                raise AttributeError()
            return lambda: self.basic_test(getattr(uptime, func), rettype)
        else:
            return unittest.TestCase.__getattr__(self, name)

class BrokenCtypesTest(NormalTest):
    """
    It's ridiculous how many platforms don't have ctypes. This class simulates
    that.
    """
    def setUpClass(self):
        uptime.ctypes = None
        delattr(uptime, 'struct')
        delattr(uptime, 'os')


def run_suite(suite):
    """
    unittest is basically a disaster, so let's do this ourselves.
    """
    sys.stdout.write('Running %d tests... \n' % tests.countTestCases())

    res = unittest.TestResult()
    suite.run(res)

    if res.wasSuccessful():
        sys.stdout.write('Finished without errors.\n')
        return

    sys.stdout.write('\n')
    for problems, kind in ((res.errors, 'error'),
                           (res.failures, 'failure')):
        if len(problems):
            head = '%d %s%s' % (len(problems),
                                kind,
                                's' if len(problems) != 1 else '')
            sys.stdout.write('\033[1;31m%s\n%s\033[0m\n' %
                             (head, '⎻' * len(head)))

        for problem in problems:
            func = problem[0]._testMethodName[5:]
            environ = ' (broken ctypes)' if isinstance(problem[0],
                                                       BrokenCtypesTest) \
                                         else ''
            sys.stdout.write(
                '• \033[1m%s%s\033[0m failed with message:\n\n%s\n\n' %
                (func, environ, '\n'.join(map(lambda s: '    ' + s,
                                              problem[1].splitlines())))
            )

    sys.stdout.write('%d tests completed successfully.\n' %
                     (res.testsRun - len(res.failures) - len(res.errors)))


if __name__ == '__main__':
    tests = unittest.TestSuite()

    # uptime tests
    tests.addTests([NormalTest('test_uptime'),
                    BrokenCtypesTest('test_uptime')])
    for helper in uptime_helpers:
        tests.addTests([NormalTest('test_%s' % helper),
                        BrokenCtypesTest('test_%s' % helper)])

    # boottime tests
    tests.addTests([NormalTest('test_boottime'),
                    BrokenCtypesTest('test_boottime')])
    for helper in boottime_helpers:
        tests.addTests([NormalTest('test_%s' % helper),
                        BrokenCtypesTest('test_%s' % helper)])

    run_suite(tests)
