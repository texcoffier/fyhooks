#!/usr/bin/python3

import sys
import threading
import time
import reactor

R = reactor.Reactor()
class Model:
    variables = {}
    history = []
    def __str__(self):
        t = []
        t.append(f'\n\tmodel={M.variables}')
        t.append(f'\n\thistory')
        for history in M.history:
            t.append(f'\n\t\t{history}')
        return ''.join(t)
M = Model()

@R.handler('START')
def _start(event:reactor.Event):
    class StdinReader(threading.Thread):
        def run(self):
            for line in sys.stdin:
                R('stdin', line)

    class Timer(threading.Thread):
        def run(self):
            while True:
                R('timer')
                time.sleep(5)
    R('print', '''
    Commands:
       VARNAME=value        # Affectation
       EXPRESSION           # Evaluate expression and print it
       p                    # Dump the model
''')
    Timer().start()
    StdinReader().start()

@R.handler('print')
def _print(event:reactor.Event):
    print(event.data[1])

@R.handler('dump')
def _dump(event:reactor.Event):
    R('print', str(M))
    M.history.pop()

@R.handler('timer')
def _timer(event:reactor.Event):
    M.variables['T'] = M.variables.get('T', 0) + 1

@R.handler('stdin')
def _calc(event:reactor.Event):
    try:
        result = eval(event.data[1], {}, M.variables)
        R('print', str(result))
        return True
    except:
        pass

@R.handler('stdin')
def _set(event:reactor.Event):
    try:
        var, val = event.data[1].split('=', 1)
        val = eval(val, None, M.variables)
        M.variables[var] = val
        R('print', f'{var}={val}')
        return True
    except:
        pass

@R.handler('stdin')
def _do_dump(event:reactor.Event):
    if event.data[1] == 'p\n':
        R('dump')
        return True

@R.handler('', 'A')
def _record(event:reactor.Event):
    M.history.append(str(event.data))


R('START')

