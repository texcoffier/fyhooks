"""
HTTP Request timer
"""

import time
from reactor import R

@R.handler('get', 'A')
def start_timer(args):
    """Register the start time"""
    args[1].start_time = time.time()

@R.handler('print', 'L')
def stop_timer(args):
    """Add the duration to the printed string"""
    if len(args) == 4:
        args[1] += f'\n{1000*(time.time() - args[3].start_time):.1f}ms'
