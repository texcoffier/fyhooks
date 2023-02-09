"""
Expression evaluator
"""

import codecs
import cProfile
import pstats
import time
import io
from reactor import R

@R.handler('get', 'A')
def profile(state):
    """Do profiling"""
    server = state.server
    if not server.path.startswith('/PROFILE/'):
        return None # No profile to do
    if hasattr(server, 'profile'):
        return None # Profiling is currently done
    server.path = server.path.replace('/PROFILE', '')
    server.profile = True

    profiler = cProfile.Profile(time.time)
    profiler.enable()
    R('get', server=server)
    profiler.disable()
    buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=buffer)
    stats.strip_dirs().sort_stats('ncalls').print_stats(100)

    wfile = codecs.getwriter("utf-8")(server.wfile)
    R('print', string=buffer.getvalue(), file=wfile)
    return ''

# @R.handler('help')
# def print_help(state):
#     "help"
#     state.help.append('  EXPRESSION : [[[calc_help]]]')
# 
# @R.handler('translations')
# def translations(state):
#     "Translations"
#     state.translations['en']['calc_help'] = "print the evaluation result"
#     state.translations['fr']['calc_help'] = "affiche le résultat de l'évaluation"
