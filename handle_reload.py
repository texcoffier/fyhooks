"""
Reload modified functionalities on disk.
Send events BEFORE_RELOAD before each unloading
and RELOAD after all the reloading are done.
"""

import os
import sys
import importlib
from reactor import R

R.description('BEFORE_RELOAD',
    'Arguments: state.functionnality\nEvent send just before reloading the functionnality')
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
                    if must_reload:
                        R('BEFORE_RELOAD', functionality=fct.__module__)
                to_reload[fct.__module__] = must_reload
            if not to_reload[fct.__module__]:
                trimmed.append((priority, index, fct))
        R.handlers[key] = trimmed
    for module, must_reload in to_reload.items():
        if must_reload:
            importlib.reload(sys.modules[module])
    R.update_handlers()
    R('RELOAD')
    return '[[[reloaded]]] ' + ' '.join(module
                                   for module, must_reload in to_reload.items()
                                   if must_reload)

@R.handler('help', 'C3')
def print_help(state):
    "help"
    state.help.append('  r : [[[reload_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['reload_help'] = "Reload modified Python modules"
    state.translations['fr']['reload_help'] = "Réactualise les modules Python qui ont été modifiés"
    state.translations['en']['reload_button'] = "Reload Python modules"
    state.translations['fr']['reload_button'] = "Recharge les modules Python"
    state.translations['en']['reloaded'] = "Reloaded:"
    state.translations['fr']['reloaded'] = "Rechargé :"

@R.handler('buttons', 'Z')
def reload(state):
    """Add reload button"""
    state.buttons.append(('/r', '[[[reload_button]]]'))
