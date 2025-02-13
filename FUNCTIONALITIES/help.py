"""
Help page management.
It allows the other functionalities to add their messages,
Add the command displaying all the help messages.
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
def _help(state):
    "help"
    state.help.append('  h : [[[help_help]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['help_help'] = "Print this help"
    state.translations['fr']['help_help'] = "Affiche ce message d'aide"
    state.translations['en']['help_cmd'] = "Commands:\n"
    state.translations['fr']['help_cmd'] = "Commandes :\n"

@R.handler('home_page')
def home_help(state):
    """Add the list of commands on home page"""
    state.items.append(
        {'column': 'C0', 'row': 'R2', 'html': 'HELP', 'src': '/h',
         'css': '<.> { font-family:monospace, monospace; white-space: pre; background: #DFD}'})
