"""
HTTP Request timer
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
        state.string += f'\n{1000*(time.time() - server.start_time):.1f}ms'
