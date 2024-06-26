#!/usr/bin/python3

"""
Handle stdin for the CLI
Launch a thread to read and evaluate stdin.
Displays timer events.
Displays syntax error if nobody evaluated the command.
"""
import sys
from reactor import R

@R.handler('START')
@R.handler('AFTER_RELOAD')
def _start(state):
    """Start the stdin reader"""
    if getattr(state, 'functionality', __name__) != __name__:
        return
    def stdin_reader(running):
        """Send 'eval' event on line read"""
        for line in sys.stdin:
            if not running:
                break
            R('print', string=R('eval', command=line.strip(), wfile=sys.stdout))
    R('print', string="[[[stdin_start]]]")
    R('start_thread', function=stdin_reader)

@R.handler('print')
def _print(state):
    """Print on stdout or the given file"""
    print(state.string, file=getattr(state, 'wfile', sys.stdout))

@R.handler('timer')
def _timer(_state):
    """Action on timer event"""
    time = R.M.variables.get("T", 0)
    if time:
        R('print', string=f'[[[stdin_timer]]] T={time}')

@R.handler('eval', 'Z')
def syntax_error(state):
    """If execution is here, nothing has been reconized"""
    return f"[[[stdin_error]]] «{state.command}»"

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['stdin_error'] = "SYNTAX ERROR"
    state.translations['fr']['stdin_error'] = "ERREUR DE SYNTAXE"
    state.translations['en']['stdin_timer'] = "Timer event"
    state.translations['fr']['stdin_timer'] = "Événement périodique"
    state.translations['en']['stdin_start'] = "Hit 'h' <enter> to print help."
    state.translations['fr']['stdin_start'] = "Tapez 'h' puis Entrée pour afficher l'aide."
