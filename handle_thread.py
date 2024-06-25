"""
Manage threading
"""

import collections
import threading
from typing import Dict, List, Callable
from reactor import R

R.description('start_thread', 'Arguments: state.function\nThe function to start.')

running:Dict[str,List[Callable]] = collections.defaultdict(list)

@R.handler('start_thread')
def start(state):
    """Create a thread running state.function"""
    class Thread(threading.Thread):
        """Start a thread"""
        def run(self):
            """Run the function in the thread"""
            thread_list = running[state.function.__module__]
            thread_list.append(state.function)
            try:
                state.function(thread_list)
            finally:
                if state.function in thread_list:
                    thread_list.remove(state.function)
    Thread().start()

@R.handler('BEFORE_RELOAD')
@R.handler('BEFORE_DISABLE')
def stop_thread(state):
    """Stop the threads."""
    if state.functionality in running:
        running[state.functionality].clear()

@R.handler('eval')
def do_thread(state):
    """List thread"""
    if state.command != 'pp':
        return None
    return '[[[dump_p]]]\n' + '\n'.join(f'{key}:{value}' for key, value in running.items())

@R.handler('help', 'C3')
def print_help(state):
    "help"
    state.help.append('  pp : [[[dump_p]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['dump_p'] = "Process list"
    state.translations['fr']['dump_p'] = "Liste des processus"

@R.handler('home_page')
def home_thread_list(state):
    """Add the thread list on home page"""
    state.items.append(
        {'column': 'C0', 'row': 'R8', 'html': 'PM', 'src': '/pp',
         'css': '<.> { font-family:monospace, monospace; white-space: pre;background: #EEE}'})
