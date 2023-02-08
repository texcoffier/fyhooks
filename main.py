#!/usr/bin/python3
"""
Setup application data and used functionnalities
"""
# pylint: disable=unused-import
from typing import Dict, List, Tuple, Callable, Any
from reactor import R
import handle_stdin
import handle_help
import handle_calc
import handle_affectation
import handle_dump
import handle_reload
import handle_translations
import handle_timer
import handle_http
import handle_log

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables:Dict[str, Any] = {}
    history:List[str] = []
    def __str__(self):
        lines = []
        lines.append(f'    model={self.variables}\n')
        lines.append('    history\n')
        for history in self.history:
            lines.append(f'        {history[:100].replace("[[[", "[")}\n')
        lines.append('    reactor\n')
        for line in str(R).split('\n'):
            lines.append(f'        {line}\n')
        R('informations', lines)
        return ''.join(lines)
R.M = Model() # pylint: disable=invalid-name

@R.handler('', 'A')
def _record(args):
    """Record all event except printing ones"""
    if args[0] != 'print':
        R.M.history.append(repr(args))

R('INIT') # For translations because they are needed before START
R('START')
