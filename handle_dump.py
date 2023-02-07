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

@R.handler('stdin')
def do_dump(args):
    """If it is the dump command do it, and returns
    then dump to stop event propagation"""
    if args[1].strip() == 'p':
        return R('dump')
    return None

@R.handler('help')
def print_help(args):
    "help"
    args[1].append('  p : display model dump')
