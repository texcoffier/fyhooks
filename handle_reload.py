"""
Setup application data and used functionnalities
"""

import os
import sys
import importlib
from reactor import R

@R.handler('eval')
def do_reload(args):
    """If reload command: do it"""
    if args[1].strip() != 'r':
        return None
    to_reload = {}
    for key, handlers in tuple(R.handlers.items()):
        trimmed = []
        for priority, index, fct in handlers:
            if fct.__module__ not in to_reload:
                module = sys.modules[fct.__module__]
                if not module.__spec__:
                    must_reload = False # Main module
                else:
                    must_reload = (os.path.getmtime(module.__spec__.cached)
                                 < os.path.getmtime(module.__spec__.origin))
                to_reload[fct.__module__] = must_reload
            if not to_reload[fct.__module__]:
                trimmed.append((priority, index, fct))
        R.handlers[key] = trimmed
    for module, must_reload in to_reload.items():
        if must_reload:
            importlib.reload(sys.modules[module])
    R('RELOAD')
    return 'Reloaded: ' + ' '.join(module
                                   for module, must_reload in to_reload.items()
                                   if must_reload)

@R.handler('help', 'C2')
def print_help(args):
    "help"
    args[1].append('  r : [[[reload_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['reload_help'] = "reload modified Python modules"
    args[1]['fr']['reload_help'] = "reactualise les modules Python qui ont été modifiés"
