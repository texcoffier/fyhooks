"""
HTTP server
"""

import time
import threading
from reactor import R

def start(output):
    """Launch the thread"""
    class HTTP(threading.Thread):
        """The display run in a thread"""
        def run(self):
            """Start the server"""
            history = R.M.history
            i = len(history)
            while True:
                while i < len(history):
                    R("print", string=history[i], file=output)
                    i += 1
                output.flush()
                time.sleep(0.1)
    HTTP().start()


@R.handler('eval')
def logs(state):
    """Live log stream display"""
    if state.command == 'l':
        start(state.file)
        server = getattr(state, 'server', None)
        if server:
            server.do_not_close = True
        return '[[[log_started]]]'
    return None

@R.handler('help', 'C2')
def print_help(state):
    "help"
    state.help.append('  l : [[[log_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['log_help'] = "live log display"
    state.translations['fr']['log_help'] = "affiche les log en temps réel"
    state.translations['en']['log_started'] = "Live log started"
    state.translations['fr']['log_started'] = "L'affichage des logs en temps réel a commencé"
