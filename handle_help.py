"""
Display help
"""

from reactor import R

@R.handler('eval')
def get_help(state):
    """If it is the help command, return it to stop propagation"""
    if state.command == 'h':
        data = []
        R('help', help=data)
        return '[[[help_cmd]]]' + '\n'.join(data)
    return None

@R.handler('help', 'C')
def print_help(state):
    "help"
    state.help.append('  h : [[[help_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['help_help'] = "print this help"
    state.translations['fr']['help_help'] = "affiche ce message d'aide"
    state.translations['en']['help_cmd'] = "Commands:\n"
    state.translations['fr']['help_cmd'] = "Commandes :\n"
