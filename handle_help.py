"""
Display help
"""

from reactor import R

@R.handler('eval')
def get_help(args):
    """If it is the help command, return it to stop propagation"""
    if args[1].strip() == 'h':
        data = []
        R('help', data)
        return '[[[help_cmd]]]' + '\n'.join(data)
    return None

@R.handler('help', 'C')
def print_help(args):
    "help"
    args[1].append('  h : [[[help_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['help_help'] = "print this help"
    args[1]['fr']['help_help'] = "affiche ce message d'aide"
    args[1]['en']['help_cmd'] = "Commands:\n"
    args[1]['fr']['help_cmd'] = "Commandes :\n"
