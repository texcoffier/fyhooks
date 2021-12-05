#!/usr/bin/python3

"""
Make many things
"""

# pylint: disable=unused-import

import sys
import threading
from reactor import R
import handle_timer
import handle_calc
import handle_affectation
import handle_dump
import handle_http

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables = {}
    history = []
    def __str__(self):
        lines = []
        lines.append(f'\n\tmodel={self.variables}')
        lines.append(f'\n\thistory')
        for history in self.history:
            lines.append(f'\n\t\t{history}')
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
                R('stdin', line)
    R('print', 'Commands:')
    R('help')
    StdinReader().start()

@R.handler('print')
def _print(event):
    """Print on stdout"""
    print(event.data[1])

@R.handler('', 'A')
def _record(event):
    """Record all event"""
    R.M.history.append(str(event.data))

R('START')
