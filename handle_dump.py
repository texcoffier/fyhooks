"""
Debugger
"""

from reactor import R

@R.handler('dump')
def dump(_args):
    """Manage the dump event and returns the dump"""
    result = str(R.M)
    R.M.history.pop()
    return result

@R.handler('eval')
def do_dump(args):
    """If it is the dump command do it, and returns
    then dump to stop event propagation"""
    if args[1].strip() == 'p':
        return R('dump')
    return None

@R.handler('help', 'C2')
def print_help(args):
    "help"
    args[1].append('  p : [[[dump_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['dump_help'] = "display model dump"
    args[1]['fr']['dump_help'] = "affiche les structures de données de l'application"
