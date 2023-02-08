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
                    R("print", history[i], output)
                    i += 1
                output.flush()
                time.sleep(1)
    HTTP().start()


@R.handler('eval')
def logs(args):
    """Live log stream display"""
    if args[1].strip() == 'l':
        start(args[2])
        args[3].do_not_close = True
        return '[[[log_started]]]'
    return None

@R.handler('help', 'C2')
def print_help(args):
    "help"
    args[1].append('  l : [[[log_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['log_help'] = "live log display"
    args[1]['fr']['log_help'] = "affiche les log en temps réel"
    args[1]['en']['log_started'] = "Live log started"
    args[1]['fr']['log_started'] = "L'affichage des logs en temps réel a commencé"
