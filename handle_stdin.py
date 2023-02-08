#!/usr/bin/python3

"""
Handle stdin
"""
import sys
import threading
from reactor import R

@R.handler('START')
def _start(_args):
    """Start the stdin reader"""
    class StdinReader(threading.Thread):
        """Thread reading the stdin"""
        def run(self):
            """Send 'eval' event on line read"""
            for line in sys.stdin:
                R('print', R('eval', line))
    R('print', "[[[stdin_start]]]")
    StdinReader().start()

@R.handler('print')
def _print(args):
    """Print on stdout or the given file"""
    if len(args) == 3:
        print(args[1], file=args[2])
    else:
        print(args[1])

@R.handler('timer')
def _timer(_args):
    """Action on timer event"""
    time = R.M.variables.get("T", 0)
    if time:
        R('print', f'[[[stdin_timer]]] T={time}')

@R.handler('eval', 'Z')
def syntax_error(_args):
    """If execution is here, nothing has been reconized"""
    return "[[[stdin_error]]]"

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['stdin_error'] = "SYNTAX ERROR"
    args[1]['fr']['stdin_error'] = "ERREUR DE SYNTAXE"
    args[1]['en']['stdin_timer'] = "Timer event"
    args[1]['fr']['stdin_timer'] = "Événement périodique"
    args[1]['en']['stdin_start'] = "Hit 'h' <enter> to print help."
    args[1]['fr']['stdin_start'] = "Tapez 'h' puis Entrée pour afficher l'aide."

