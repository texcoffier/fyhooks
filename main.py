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
import handle_home
import handle_log
import handle_request_time

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables:Dict[str, Any] = {}
    history:List[str] = []
R.M = Model() # pylint: disable=invalid-name

@R.handler('', 'A')
def _record(args):
    """Record all event except printing ones"""
    if args[0] != 'print':
        clean = []
        for item in args:
            if not isinstance(item, (str, int)):
                item = item.__class__.__name__
            clean.append(str(item))
        R.M.history.append(str(clean))

R('PRESTART') # For translations because they are needed before START
R('START')
