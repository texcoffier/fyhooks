"""
Display help
"""

from reactor import R

@R.handler('stdin')
def do_dump(args):
    """If it is the help command, return it to stop propagation"""
    if args[1].strip() == 'h':
        data = []
        R('help', data)
        return 'Commands:\n' + '\n'.join(data)
    return None

@R.handler('help', 'C')
def print_help(args):
    "help"
    args[1].append('  h : print this help')
