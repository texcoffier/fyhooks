"""
Debugger
"""

from reactor import R

@R.handler('eval')
def do_dump(state):
    """If it is the dump command do it, and returns
    then dump to stop event propagation"""
    if state.command.startswith('p'):
        if state.command == 'pm':
            return '[[[dump_m]]]\n' + str(R.M.variables)
        if state.command == 'ph':
            lines = ['[[[dump_h]]]\n']
            for history in R.M.history:
                lines.append(f'{history[:100].replace("[[[", "[")}\n')
            return ''.join(lines)
        if state.command == 'pr':
            return '[[[dump_r]]]\n' + str(R)
    return None

@R.handler('help', 'C2')
def print_help(state):
    "help"
    state.help.append('  pm : [[[dump_m]]]')
    state.help.append('  ph : [[[dump_h]]]')
    state.help.append('  pr : [[[dump_r]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['dump_m'] = "Application memory dump"
    state.translations['fr']['dump_m'] = "Liste des structures de données de l'application"
    state.translations['en']['dump_h'] = "History of event"
    state.translations['fr']['dump_h'] = "Historique des événements"
    state.translations['en']['dump_r'] = "Reactor handlers list"
    state.translations['fr']['dump_r'] = "Liste des gestionnaires d'événements"
