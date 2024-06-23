"""
Setup application data and used functionalities
"""

import os
import sys
import importlib
from reactor import R

R.description("RELOAD", "Arguments: None\nCalled after a Python module reload")

@R.handler('eval')
def do_reload(state):
    """If reload command: do it"""
    if state.command != 'r':
        return None
    to_reload = {}
    for key, handlers in tuple(R.handlers.items()):
        # Remove hooks from reloaded modules
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

@R.handler('help', 'C3')
def print_help(state):
    "help"
    state.help.append('  r : [[[reload_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['reload_help'] = "reload modified Python modules"
    state.translations['fr']['reload_help'] = "reactualise les modules Python qui ont été modifiés"
    state.translations['en']['reload_button'] = "Reload Python modules"
    state.translations['fr']['reload_button'] = "Recharge les modules Python"

@R.handler('buttons', 'Z')
def reload(state):
    """Add reload button"""
    state.buttons.append(('/r', '[[[reload_button]]]'))
