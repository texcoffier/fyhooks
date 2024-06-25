"""
Functionality disabling.
Remove all the handlers added by the functionality.
Send an event before and after disabling a functionality.
"""

import sys
from reactor import R

R.description('BEFORE_DISABLE',
    'Arguments: state.functionnality\nEvent send just before disabling the functionnality')
R.description('AFTER_DISABLE',
     'Arguments: state.functionnality\nEvent send just after disabling the functionnality')

@R.handler('eval')
def display_or_disable(state):
    """If disable functionnality command: do it"""
    if state.command == 'pf':
        def display(fct):
            label = fct.__module__ + ' : '
            indent = ' ' * len(label)
            lines = sys.modules[fct.__module__].__doc__.strip().split('\n')
            return label + lines.pop(0) + '\n' + ''.join(indent + i.strip() + '\n'
                                                            for i in lines)
        fcties = set(
            display(fct)
            for key, handlers in tuple(R.handlers.items())
            for priority, index, fct in handlers
            if fct.__module__ != '__main__'
            )
        return '[[[dump_f]]]\n' + ''.join(sorted(fcties))

    if not state.command.startswith('df'):
        return None
    fcty = state.command.split(' ')[-1]
    R('BEFORE_DISABLE', functionality=fcty)
    for key, handlers in tuple(R.handlers.items()):
        R.handlers[key] = [(priority, index, fct)
                           for priority, index, fct in handlers
                           if fct.__module__ != fcty
                          ]
    R.update_handlers()
    R('AFTER_DISABLE', functionality=fcty)
    return '[[[disabled]]] ' + fcty

@R.handler('help', 'C9')
def print_help(state):
    "help"
    state.help.append('  df : [[[disable_functionnality_help]]]')
    state.help.append('  pf : [[[dump_f]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['disable_functionnality_help'] = "Disable the named functionality"
    state.translations['fr']['disable_functionnality_help'] = "Désactive la fonctionnalité indiquée"
    state.translations['en']['disabled'] = "Disabled:"
    state.translations['fr']['disabled'] = "Désactivée :"
    state.translations['en']['dump_f'] = "Functionalities list"
    state.translations['fr']['dump_f'] = "Liste des fonctionnalités"

@R.handler('home_page')
def home_help(state):
    """Add the functionality list on home page"""
    state.items.append(
        {'column': 'C6', 'row': 'R9', 'html': 'FCTY', 'src': '/pf',
         'css': '<.> { font-family:monospace, monospace; white-space: pre; background: #FDF;}'})
