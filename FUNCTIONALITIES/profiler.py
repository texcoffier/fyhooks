"""
Display an execution profile of the «get» handler.
This works only with the HTTP server.
"""

import codecs
import cProfile
import pstats
import time
import io
from reactor import R

@R.handler('get', 'A')
def profile(state):
    """Do profiling only for web server"""
    server = state.server
    if not server.path.startswith('/PROFILE/'):
        return None # No profile to do
    if hasattr(server, 'profile'):
        return None # Profiling is currently done
    server.path = server.path.replace('/PROFILE', '')

    profiler = cProfile.Profile(time.time)
    profiler.enable()
    R('get', server=server)
    profiler.disable()
    buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=buffer)
    stats.strip_dirs().sort_stats('ncalls').print_stats(100)

    wfile = codecs.getwriter("utf-8")(server.wfile)
    R('print', string=buffer.getvalue(), wfile=wfile, server=server)
    return '' # Do not continue evaluation
