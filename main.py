#!/usr/bin/python3

import sys
import threading
import time
import reactor

R = reactor.Reactor()
class Model:
    variables = {}
M = Model()


def _start(event:reactor.Event):
    class StdinReader(threading.Thread):
        def run(self):
            for line in sys.stdin:
                R('stdin', line)

    class Timer(threading.Thread):
        def run(self):
            while True:
                R('timer')
                time.sleep(1)
    R('print', 'start threads')
    Timer().start()
    StdinReader().start()
R.add('START', _start, 'A')

def _print(event:reactor.Event):
    print('print', event.data[1])
R.add('print', _print, 'B')

def _dump(event:reactor.Event):
    R('print', f"event={event} model={M.variables}")
R.add('dump', _dump, 'D')

def _timer(event:reactor.Event):
    M.variables['T'] = M.variables.get('T', 0) + 1
R.add('timer', _timer, 'T')

def _calc(event:reactor.Event):
    try:
        result = eval(event.data[1], {}, M.variables)
        R('print', str(result))
        return True
    except:
        pass
R.add('stdin', _calc, 'C2')

def _set(event:reactor.Event):
    try:
        var, val = event.data[1].split('=', 1)
        M.variables[var] = eval(val)
        R('dump')
        return True
    except:
        pass
R.add('stdin', _set, 'C')

def _do_dump(event:reactor.Event):
    if event.data[1] == 'p\n':
        R('dump')
        return True
R.add('stdin', _do_dump, 'A')


R('START')

