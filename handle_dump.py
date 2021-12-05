#!/usr/bin/python3

from reactor import R

@R.handler('dump')
def dump(event):
    result = str(R.M)
    R('print', result)
    R.M.history.pop()
    return result

@R.handler('stdin')
def do_dump(event):
    if event.data[1].strip() == 'p':
        return R('dump')

@R.handler('help')
def help(event):
    R('print', '  p : display model dump')

