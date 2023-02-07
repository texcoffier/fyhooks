"""
Expression evaluator
"""

from reactor import R

@R.handler('stdin')
def calc(args):
    """Evaluate the expression and returns it.
    If there is no error, stop the event and return the value."""
    try:
        return eval(args[1], {}, R.M.variables) # pylint: disable=eval-used
    except: # pylint: disable=bare-except
        return None # For example if affectation

@R.handler('help')
def print_help(args):
    "help"
    args[1].append('  EXPRESSION : print the evaluation result')
