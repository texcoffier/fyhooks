#!/usr/bin/python3

from reactor import R

@R.handler('stdin')
def set(event):
    try:
        var, val = event.data[1].split('=', 1)
        val = eval(val, None, R.M.variables)
        R.M.variables[var] = val
        result = f'{var}={val}'
        R('print', result)
        return  result
    except:
        pass

@R.handler('help')
def help(event):
    R('print', '  VARNAME=EXPRESSION : Evaluate the expression, store it and display it')

