"""
Debugger
"""

from reactor import R

@R.handler('eval')
def do_dump(args):
    """If it is the dump command do it, and returns
    then dump to stop event propagation"""
    cmd = args[1].strip()
    if cmd.startswith('p'):
        if cmd == 'pm':
            return '[[[dump_m]]]\n' + str(R.M.variables)
        if cmd == 'ph':
            lines = ['[[[dump_h]]]\n']
            for history in R.M.history:
                lines.append(f'{history[:100].replace("[[[", "[")}\n')
            return ''.join(lines)
        if cmd == 'pr':
            return '[[[dump_r]]]\n' + str(R)
    return None

@R.handler('help', 'C2')
def print_help(args):
    "help"
    args[1].append('  pm : [[[dump_m]]]')
    args[1].append('  ph : [[[dump_h]]]')
    args[1].append('  pr : [[[dump_r]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['dump_m'] = "Application memory dump"
    args[1]['fr']['dump_m'] = "Liste des structures de données de l'application"
    args[1]['en']['dump_h'] = "History of event"
    args[1]['fr']['dump_h'] = "Historique des événements"
    args[1]['en']['dump_r'] = "Reactor handlers list"
    args[1]['fr']['dump_r'] = "Liste des gestionnaires d'événements"
