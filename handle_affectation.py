"""
Affection handler.
It allows to write «foo = 'bar'» on command line.
"""

from reactor import R

@R.handler('eval')
def set_var(state):
    """If the affection is possible, set the variable in the model
    and stop the event propagation by returning an explanation"""
    try:
        var, val = state.command.split('=', 1)
        val = eval(val, None, R.M.variables) # pylint: disable=eval-used
        R.M.variables[var] = val
        return f'{var} ← {val}'
    except: # pylint: disable=bare-except
        return None

@R.handler('help')
def print_help(state):
    "Help"
    state.help.append('  VARNAME=EXPRESSION [[[affectation_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    # pylint: disable=line-too-long
    state.translations['en']['affectation_help'] = "Evaluate the expression, store it and display it"
    state.translations['fr']['affectation_help'] = "Évalue l'expression et l'enregistre dans la variable"
