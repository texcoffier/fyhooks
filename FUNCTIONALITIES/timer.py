"""
Send timer event every 10 seconds
"""

import time
from reactor import R

R.description('timer', 'Arguments: None\nThe event is sent every 10 seconds.')

@R.handler('START')
@R.handler('AFTER_RELOAD')
def start(state):
    """Start a timer thread"""
    if getattr(state, 'functionality', __name__) != __name__:
        return
    def timer_thread(running):
        while running:
            R('timer')
            time.sleep(10)
    R('start_thread', function=timer_thread)

@R.handler('timer')
def timer(_state):
    """Incremente T variable on each timer event"""
    R.M.variables['T'] = R.M.variables.get('T', 0) + 1

@R.handler('help', 'X')
def _help(state):
    "help"
    state.help.append('[[[timer_help]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    # pylint: disable=line-too-long
    state.translations['en']['timer_help'] = "A timer will display a message every 10 seconds"
    state.translations['fr']['timer_help'] = "Une tâche périodique affiche un message toutes les 10 secondes"
