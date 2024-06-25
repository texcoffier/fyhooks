#!/usr/bin/python3
"""
Setup application data and used functionalities
"""
# pylint: disable=unused-import
from typing import Dict, List, Any
from reactor import R
import handle_stdin
import handle_help
import handle_calc
import handle_affectation
import handle_dump
import handle_reload
import handle_translations
import handle_thread
import handle_timer
import handle_http
import handle_home
import handle_log
import handle_request_time
import handle_profiler
import handle_functionality

class Model: # pylint: disable=too-few-public-methods
    """The model"""
    variables:Dict[str, Any] = {}
    history:List[str] = []

R.M = Model() # pylint: disable=invalid-name

@R.handler('', 'A')
def _record(state):
    """Record all event except printing ones"""
    if state.event != 'print':
        R.M.history.append(str(state))

R.description('PRESTART', "Arguments: None\nLaunched first to initialize things.")
R.description('START', "Arguments: None\nLaunched after PRESTART to begin jobs.")
R.description('eval', """Arguments: state.command, state.file, [state.server]
                         Evaluate the command for command line or web server.""")
R.description('help', """Arguments: state.help
                         Append new help messages to state.help""")
R.description('print', """Arguments: state.string [state.file] [state.server]""")

R('PRESTART') # For translations because they are needed before START
R('START')
