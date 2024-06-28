"""
HTTP server.
It calls 'http' to allows functionalities to add HTTP headers.
It calls 'get' to retrieve the content to be displayed.
It calls 'print' to display the page content.
"""

import codecs
import threading
import http.server
import urllib
from reactor import R

R.description('get', 'Arguments: state.server')
R.description('http', '''Arguments: state.url, state.server
Answer to the URL if needed.''')

@R.handler('START')
@R.handler('AFTER_RELOAD')
def start(state):
    """Launch the thread"""
    if getattr(state, 'functionality', __name__) != __name__:
        return
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
            R('get', server=self)
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
def get(state):
    """Manage the HTTP get"""
    server = state.server
    url = urllib.parse.unquote(server.path[1:])
    server.send_response(200)
    if not R('http', url=url, server=server):
        server.send_header('Content-Type', 'text/plain; charset=UTF-8')
    server.send_header('Cache-Control', 'no-cache')
    server.send_header('Cache-Control', 'no-store')
    server.end_headers()
    wfile = codecs.getwriter("utf-8")(server.wfile)
    result = R('eval', command=url, wfile=wfile, server=server)
    R('print', string=result, wfile=wfile, server=server)

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['http_start'] = "Server waiting on"
    state.translations['fr']['http_start'] = "Le serveur web est en attente à l'adresse"
