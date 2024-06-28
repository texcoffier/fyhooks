#!/usr/bin/python3
"""
Setup application data and used functionalities
"""
# pylint: disable=unused-import
from typing import Dict, List, Any
import os
import importlib
from reactor import R

for functionality in os.listdir('FUNCTIONALITIES'):
    if functionality.endswith('.py'):
        importlib.import_module('FUNCTIONALITIES.' + functionality[:-3])

class Model: # pylint: disable=too-few-public-methods
    """The data model of your application"""
    variables:Dict[str, Any] = {}
    history:List[str] = []

R.M = Model() # pylint: disable=invalid-name

@R.handler('', 'A')
def _record(state):
    """Record all event except printing ones in the history"""
    if state.event != 'print':
        R.M.history.append(str(state))

R.description('PRESTART', "Arguments: None\nLaunched first to initialize things.")
R.description('START', "Arguments: None\nLaunched after PRESTART to begin jobs.")
R.description('eval', """Arguments: state.command, state.file, [state.server]
                         Evaluate the command for command line or web server.""")
R.description('help', """Arguments: state.help
                         Append new help messages to state.help""")
R.description('print', """Arguments: state.string [state.wfile] [state.server]""")

R('PRESTART') # For translations because they are needed before START
R('START')
