#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include <utmpx.h>
#include <sys/time.h>

/*
The reason this exists as a full-blown C extension instead of as a pure-Python
function using ctypes is that while POSIX specifies utmpx, it does not specify
the values of its various constants or the order or size of struct utmpx's
members. In practice, all of these things vary, and there's no way for us to
find any of them at runtime from Python.
*/

static PyObject*
_uptime_posix(PyObject *self, PyObject *args)
{
    struct utmpx id = {.ut_type = BOOT_TIME}, *res;
    struct timeval tv, bt;
    double up;

    /* Unused arguments. */
    (void)self;
    (void)args;

    /* Get current time. */
    if (gettimeofday(&tv, NULL) != 0) {
        Py_RETURN_NONE;
    }

    /* Get boot time if it's there. */
    if ((res = getutxid(&id)) == NULL) {
        endutxent();
        Py_RETURN_NONE;
    }
    memcpy(&bt, &(res->ut_tv), sizeof(struct timeval));
    endutxent();

    /* Subtract boot time from current time. */
    if (tv.tv_usec < bt.tv_usec) {
        tv.tv_sec--;
        tv.tv_usec = 1000000 - bt.tv_usec + tv.tv_usec;
    } else {
        tv.tv_usec -= bt.tv_usec;
    }
    tv.tv_sec -= bt.tv_sec;

    up = (unsigned)tv.tv_sec + (unsigned)tv.tv_usec / 1000000.0;
    return Py_BuildValue("d", up);
}

static PyMethodDef _uptime_methods[] = {
    {"_uptime_posix", _uptime_posix, METH_NOARGS,
     "Fallback uptime for POSIX."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_posix(void)
{
    Py_InitModule("_posix", _uptime_methods);
}
