"""
Expression evaluator.
It returns the result of the Python 'eval'.
"""

from reactor import R

@R.handler('eval')
def calc(state):
    """Evaluate the expression and returns it.
    If there is no error, stop the event and return the value."""
    try:
        return str(eval(state.command, {}, R.M.variables)) # pylint: disable=eval-used
    except: # pylint: disable=bare-except
        return None # For example if affectation

@R.handler('help')
def _help(state):
    "help"
    state.help.append('  EXPRESSION : [[[calc_help]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['calc_help'] = "Print the evaluation result"
    state.translations['fr']['calc_help'] = "Affiche le résultat de l'évaluation"
