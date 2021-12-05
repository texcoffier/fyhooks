#!/usr/bin/python3

import sys
import threading
import time
import reactor
import http.server

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
                time.sleep(10)

    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            R("get", self)

    class HTTP(threading.Thread):
        def run(self):
            http.server.HTTPServer(('127.0.0.1', 8888), HTTPHandler).serve_forever()

    R('print', '''Commands:
  VARNAME=value # Affectation
  EXPRESSION    # Evaluate expression and print it
  p             # Dump the model

Server waiting on http://127.0.0.1:8888/command
''')
    Timer().start()
    StdinReader().start()
    HTTP().start()

@R.handler('print')
def _print(event:reactor.Event):
    print(event.data[1])

@R.handler('dump')
def _dump(event:reactor.Event):
    result = str(M)
    R('print', result)
    M.history.pop()
    return result

@R.handler('timer')
def _timer(event:reactor.Event):
    M.variables['T'] = M.variables.get('T', 0) + 1

@R.handler('stdin')
def _calc(event:reactor.Event):
    try:
        result = eval(event.data[1], {}, M.variables)
        R('print', str(result))
        return result
    except:
        pass

@R.handler('stdin')
def _set(event:reactor.Event):
    try:
        var, val = event.data[1].split('=', 1)
        val = eval(val, None, M.variables)
        M.variables[var] = val
        result = f'{var}={val}'
        R('print', result)
        return  result
    except:
        pass

@R.handler('reply')
def _reply(event:reactor.Event):
    server = event.data[1]
    server.send_response(200)
    server.end_headers()
    server.wfile.write(str(event.data[2]).encode('utf-8'))

@R.handler('get')
def _get(event:reactor.Event):
    server = event.data[1]
    result = R('stdin', server.path[1:])
    R('reply', server, result)

@R.handler('stdin')
def _do_dump(event:reactor.Event):
    if event.data[1].strip() == 'p':
        return R('dump')

@R.handler('', 'A')
def _record(event:reactor.Event):
    M.history.append(str(event.data))


R('START')

