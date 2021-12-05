"""
Affection handler
"""

from reactor import R

@R.handler('stdin')
def set_var(event):
    """If the affection is possible, set the variable in the model
    and stop the event propagation by returning the new variable value"""
    try:
        var, val = event.data[1].split('=', 1)
        val = eval(val, None, R.M.variables) # pylint: disable=eval-used
        R.M.variables[var] = val
        result = f'{var}={val}'
        R('print', result)
        return result
    except: # pylint: disable=bare-except
        pass

@R.handler('help')
def print_help(_event):
    "Help"
    R('print', '  VARNAME=EXPRESSION : Evaluate the expression, store it and display it')
