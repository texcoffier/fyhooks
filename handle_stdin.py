#!/usr/bin/python3

"""
Handle stdin
"""
import sys
import threading
from reactor import R

@R.handler('START')
def _start(_args):
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
def _print(args):
    """Print on stdout"""
    print(args[1])

@R.handler('timer')
def _timer(_args):
    """Action on timer event"""
    time = R.M.variables.get("T", 0)
    if time:
        R('print', f'Time event T={time}')

@R.handler('stdin', 'Z')
def syntax_error(_args):
    """If execution is here, nothing has been reconized"""
    return "SYNTAX ERROR"
