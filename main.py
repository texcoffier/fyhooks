#!/usr/bin/python3

"""
Make many things
"""

# pylint: disable=unused-import

from typing import Dict, List, Tuple, Callable, Any
from reactor import R
import handle_stdin
import handle_help
import handle_calc
import handle_affectation
import handle_dump
import handle_timer
import handle_http

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables:Dict[str, Any] = {}
    history:List[str] = []
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

@R.handler('', 'A')
def _record(args):
    """Record all event"""
    R.M.history.append(str(args))

R('START')
