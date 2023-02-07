"""
Expression evaluator
"""

from reactor import R

@R.handler('stdin')
def calc(event):
    """Evaluate the expression and returns it.
    If there is no error, stop the event and return the value."""
    try:
        return eval(event.data[1], {}, R.M.variables) # pylint: disable=eval-used
    except: # pylint: disable=bare-except
        return None # For example if affectation

@R.handler('help')
def print_help(event):
    "help"
    event.data[1].append('  EXPRESSION : print the evaluation result')
