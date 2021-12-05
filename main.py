#!/usr/bin/python3

import sys
import threading
from reactor import R
import handle_timer
import handle_calc
import handle_affectation
import handle_dump
import handle_http

class Model:
    variables = {}
    history = []
    def __str__(self):
        t = []
        t.append(f'\n\tmodel={self.variables}')
        t.append(f'\n\thistory')
        for history in self.history:
            t.append(f'\n\t\t{history}')
        return ''.join(t)
R.M = Model()

@R.handler('START')
def _start(event):
    class StdinReader(threading.Thread):
        def run(self):
            for line in sys.stdin:
                R('stdin', line)
    R('print', 'Commands:')
    R('help')
    StdinReader().start()

@R.handler('print')
def _print(event):
    print(event.data[1])

@R.handler('', 'A')
def _record(event):
    R.M.history.append(str(event.data))

R('START')

