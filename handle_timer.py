#!/usr/bin/python3

import threading
import time
from reactor import R

@R.handler('START')
def _start(event):
    class Timer(threading.Thread):
        def run(self):
            while True:
                R('timer')
                time.sleep(10)
    Timer().start()

@R.handler('timer')
def _timer(event):
    R.M.variables['T'] = R.M.variables.get('T', 0) + 1

