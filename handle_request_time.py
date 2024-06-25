"""
HTTP Request timer.
The request starts when the «get» event is received.
Add the request time once the translation are done.
"""

import time
from reactor import R

@R.handler('get', 'A')
def start_timer(state):
    """Register the start time from web requests"""
    state.server.start_time = time.time()

@R.handler('print', 'L')
def stop_timer(state):
    """Add the duration to the printed string"""
    server = getattr(state, 'server', None)
    if server:
        state.string += f'''[[[DIV style="color:#888; right: 0; bottom: 0; position: absolute"]]]
            {1000*(time.time() - server.start_time):.1f}ms[[[/DIV]]]'''

@R.handler('buttons', 'Y')
def reload(state):
    """Add button to disable the request time display"""
    state.buttons.append(('/df handle_request_time', '[[[hide_request_time]]]'))

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['hide_request_time'] = "Hide request time"
    state.translations['fr']['hide_request_time'] = "Cache le temps CPU"
