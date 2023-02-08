"""
HTTP server
"""

import codecs
import threading
import http.server
from reactor import R

@R.handler('START')
def _start(_args):
    """Launch the thread"""
    class HTTPServer(http.server.HTTPServer):
        """Do not close connection automaticaly"""
        old_shutdown_request = http.server.HTTPServer.shutdown_request
        def shutdown_request(self, request):
            return

    finish = http.server.BaseHTTPRequestHandler.finish
    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        """Manage client connections"""
        do_not_close = False
        def do_GET(self): # pylint: disable=invalid-name
            """Send 'get' event on client connection"""
            R("get", self)
            if not self.do_not_close:
                self.server.old_shutdown_request(self.wfile._sock) # pylint: disable=protected-access
        def finish(self):
            if not self.do_not_close:
                finish(self)
    class HTTP(threading.Thread):
        """The HTTP server run in a thread"""
        def run(self):
            """Start the server"""
            HTTPServer(('127.0.0.1', 8888), HTTPHandler).serve_forever()

    HTTP().start()

@R.handler('get')
def _get(args):
    """Manage the HTTP get"""
    server = args[1]
    server.send_response(200)
    server.end_headers()
    wfile = codecs.getwriter("utf-8")(server.wfile)
    wfile.write('<!DOCTYPE html>\n<meta charset="utf-8"><pre>')
    result = R('eval', server.path[1:], wfile, server)
    R('print', result, wfile)

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
