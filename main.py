#!/usr/bin/python3

"""
Make many things
"""

# pylint: disable=unused-import

import sys
import threading
from reactor import R
import handle_help
import handle_calc
import handle_affectation
import handle_dump
import handle_timer
import handle_http

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables = {}
    history = []
    def __str__(self):
        lines = []
        lines.append(f'\n    model={self.variables}')
        lines.append('\n    history')
        for history in self.history:
            lines.append(f'\n        {history}')
        lines.append('\n    reactor')
        for line in str(R).split('\n'):
            lines.append(f'\n        {line}')
        return ''.join(lines)
R.M = Model() # pylint: disable=invalid-name

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

@R.handler('', 'A')
def _record(event):
    """Record all event"""
    R.M.history.append(str(event.data))

R('START')
