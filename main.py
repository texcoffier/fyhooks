#!/usr/bin/python3

import sys
import threading
from reactor import R
import handle_http
import handle_timer

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

    R('print', '''Commands:
  VARNAME=value # Affectation
  EXPRESSION    # Evaluate expression and print it
  p             # Dump the model

Server waiting on http://127.0.0.1:8888/command
''')
    StdinReader().start()

@R.handler('print')
def _print(event):
    print(event.data[1])

@R.handler('dump')
def _dump(event):
    result = str(R.M)
    R('print', result)
    R.M.history.pop()
    return result

@R.handler('stdin')
def _calc(event):
    try:
        result = eval(event.data[1], {}, R.M.variables)
        R('print', str(result))
        return result
    except:
        pass

@R.handler('stdin')
def _set(event):
    try:
        var, val = event.data[1].split('=', 1)
        val = eval(val, None, R.M.variables)
        R.M.variables[var] = val
        result = f'{var}={val}'
        R('print', result)
        return  result
    except:
        pass

@R.handler('stdin')
def _do_dump(event):
    if event.data[1].strip() == 'p':
        return R('dump')

@R.handler('', 'A')
def _record(event):
    R.M.history.append(str(event.data))


R('START')

