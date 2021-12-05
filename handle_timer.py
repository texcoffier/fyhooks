"""
Send timer event every 10 seconds
"""

import threading
import time
from reactor import R

@R.handler('START')
def _start(_event):
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
def _timer(_event):
    """Incremente T variable on each timer event"""
    R.M.variables['T'] = R.M.variables.get('T', 0) + 1
