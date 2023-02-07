"""
Debugger
"""

from reactor import R

@R.handler('dump')
def dump(_event):
    """Manage the dump event and returns the dump"""
    result = str(R.M)
    R.M.history.pop()
    return result

@R.handler('stdin')
def do_dump(event):
    """If it is the dump command do it, and returns
    then dump to stop event propagation"""
    if event.data[1].strip() == 'p':
        return R('dump')
    return None

@R.handler('help')
def print_help(event):
    "help"
    event.data[1].append('  p : display model dump')
