"""Measuring the running times.

E.g. http://sample-python.readthedocs.io/en/latest/_modules/testmodule/timer.html """
import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print("Elapsed time: %f ms" % self.msecs)