"""
Display log in realtime using a thread.
It tells the web server to keep the connection open.
"""

import time
from reactor import R

def start(output):
    """Launch the thread"""
    def display_logs(running):
        """Start the server"""
        history = R.M.history
        i = len(history)
        while running:
            while i < len(history):
                try:
                    R("print", string=history[i], wfile=output)
                except BrokenPipeError:
                    return # Socket closed
                i += 1
            output.flush()
            time.sleep(0.1)
    R('start_thread', function=display_logs)

@R.handler('eval')
def logs(state):
    """Live log stream display"""
    if state.command == 'l':
        start(state.wfile)
        server = getattr(state, 'server', None)
        if server:
            server.do_not_close = True
        return '[[[log_started]]]'
    return None

@R.handler('help', 'C2')
def _help(state):
    "help"
    state.help.append('  l : [[[log_help]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['log_help'] = "Live log display"
    state.translations['fr']['log_help'] = "Affiche les logs en temps réel"
    state.translations['en']['log_started'] = "Live log started"
    state.translations['fr']['log_started'] = "L'affichage des logs en temps réel a commencé"

@R.handler('home_page')
def home_log(state):
    """Add the real time log display on home page"""
    state.items.append(
        {'column': 'C2', 'row': 'R1', 'html': 'LOGS', 'src': '/l',
         'css': '<.> { font-family:monospace, monospace; white-space: pre; background: #DFF}'})
