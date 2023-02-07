"""
Affection handler
"""

from reactor import R

@R.handler('eval')
def set_var(args):
    """If the affection is possible, set the variable in the model
    and stop the event propagation by returning the new variable value"""
    try:
        var, val = args[1].split('=', 1)
        val = eval(val, None, R.M.variables) # pylint: disable=eval-used
        R.M.variables[var] = val
        return val
    except: # pylint: disable=bare-except
        return None

@R.handler('help')
def print_help(args):
    "Help"
    args[1].append('  VARNAME=EXPRESSION [[[affectation_help]]]')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['affectation_help'] = "Evaluate the expression, store it and display it"
    args[1]['fr']['affectation_help'] = "Évalue l'expression et l'enregistre dans la variable"
