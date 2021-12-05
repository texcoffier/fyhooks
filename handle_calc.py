#!/usr/bin/python3

from reactor import R

@R.handler('stdin')
def calc(event):
    try:
        result = eval(event.data[1], {}, R.M.variables)
        R('print', str(result))
        return result
    except:
        pass

@R.handler('help')
def help(event):
    R('print', '  EXPRESSION : print the evaluation result')

