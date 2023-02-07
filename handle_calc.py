"""
Expression evaluator
"""

from reactor import R

@R.handler('eval')
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
    args[1].append('  EXPRESSION : [[[calc_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['calc_help'] = "print the evaluation result"
    args[1]['fr']['calc_help'] = "affiche le résultat de l'évaluation"
