"""
Expression evaluator
"""

from reactor import R

@R.handler('eval')
def calc(state):
    """Evaluate the expression and returns it.
    If there is no error, stop the event and return the value."""
    try:
        return eval(state.command, {}, R.M.variables) # pylint: disable=eval-used
    except: # pylint: disable=bare-except
        return None # For example if affectation

@R.handler('help')
def print_help(state):
    "help"
    state.help.append('  EXPRESSION : [[[calc_help]]]')

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['calc_help'] = "print the evaluation result"
    state.translations['fr']['calc_help'] = "affiche le résultat de l'évaluation"
