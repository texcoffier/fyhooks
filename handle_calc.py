"""
Expression evaluator
"""

from reactor import R

@R.handler('stdin')
def calc(event):
    """Evaluate the expression and print it.
    If there is no error, stop the event and return the value."""
    try:
        result = eval(event.data[1], {}, R.M.variables) # pylint: disable=eval-used
        R('print', str(result))
        return result
    except: # pylint: disable=bare-except
        pass

@R.handler('help')
def print_help(_event):
    "help"
    R('print', '  EXPRESSION : print the evaluation result')
