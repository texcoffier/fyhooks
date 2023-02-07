"""
HTTP server
"""

import threading
import http.server
from reactor import R

@R.handler('START')
def _start(_args):
    """Launch the thread"""
    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        """Manage client connections"""
        def do_GET(self): # pylint: disable=invalid-name
            """Send 'get' event on client connection"""
            R("get", self)

    class HTTP(threading.Thread):
        """The HTTP server run in a thread"""
        def run(self):
            """Start the server"""
            http.server.HTTPServer(('127.0.0.1', 8888), HTTPHandler).serve_forever()

    HTTP().start()

@R.handler('reply')
def _reply(args):
    """Send a response to the client"""
    server = args[1]
    server.send_response(200)
    server.end_headers()
    server.wfile.write(b'<!DOCTYPE html>\n<meta charset="utf-8"><pre>')
    server.wfile.write(str(args[2]).encode('utf-8'))

@R.handler('get')
def _get(args):
    """Manage the HTTP get"""
    server = args[1]
    result = R('eval', server.path[1:])
    R('reply', server, result)

@R.handler('help', 'T')
def print_help(args):
    "help"
    args[1].append('[[[http_start]]] http://127.0.0.1:8888/[[[http_command]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['http_start'] = "Server waiting on"
    args[1]['fr']['http_start'] = "Le serveur web est en attente à l'adresse"
    args[1]['en']['http_command'] = "command-as-with-the-keyboard"
    args[1]['fr']['http_command'] = "une-commande-comme-au-clavier"
