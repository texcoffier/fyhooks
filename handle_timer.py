"""
Send timer event every 10 seconds
"""

import threading
import time
from reactor import R

@R.handler('START')
def _start(_args):
    """Launch the thread"""
    class Timer(threading.Thread):
        """Start a timer thread"""
        def run(self):
            """Send 'timer' event"""
            while True:
                R('timer')
                time.sleep(10)
    Timer().start()

@R.handler('timer')
def _timer(_args):
    """Incremente T variable on each timer event"""
    R.M.variables['T'] = R.M.variables.get('T', 0) + 1

@R.handler('help', 'X')
def print_help(args):
    "help"
    args[1].append('[[[timer_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['timer_help'] = "A timer will display a message every 10 seconds"
    args[1]['fr']['timer_help'] = "Une tâche périodique affiche un message toutes les 10 secondes"
