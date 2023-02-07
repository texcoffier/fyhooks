#!/usr/bin/python3

"""
Handle stdin
"""
import sys
import threading
from reactor import R

@R.handler('START')
def _start(_event):
    """Start the stdin reader"""
    class StdinReader(threading.Thread):
        """Thread reading the stdin"""
        def run(self):
            """Send 'stdin' event on line read"""
            for line in sys.stdin:
                R('print', R('stdin', line))
    R('print', "'h' to print help.")
    StdinReader().start()

@R.handler('print')
def _print(event):
    """Print on stdout"""
    print(event.data[1])

@R.handler('timer')
def _timer(_event):
    """Action on timer event"""
    R('print', f'Time event T={R.M.variables.get("T", 0) }')
