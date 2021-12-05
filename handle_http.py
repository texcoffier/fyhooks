#!/usr/bin/python3

import threading
import http.server
from reactor import R

@R.handler('START')
def _start(event):
    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            R("get", self)

    class HTTP(threading.Thread):
        def run(self):
            http.server.HTTPServer(('127.0.0.1', 8888), HTTPHandler).serve_forever()

    HTTP().start()

@R.handler('reply')
def _reply(event):
    server = event.data[1]
    server.send_response(200)
    server.end_headers()
    server.wfile.write(str(event.data[2]).encode('utf-8'))

@R.handler('get')
def _get(event):
    server = event.data[1]
    result = R('stdin', server.path[1:])
    R('reply', server, result)

@R.handler('help')
def _print(event):
    R('print', 'Server waiting on http://127.0.0.1:8888/command')

