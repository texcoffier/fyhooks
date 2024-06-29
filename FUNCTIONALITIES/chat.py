"""
Implement a chat.
"""
import sys
from reactor import R

FILES = []

@R.handler('eval')
def start_chat(state):
    """Start chat"""
    if state.command == 'chat':
        server = getattr(state, 'server', None)
        if state.wfile in FILES:
            FILES.remove(state.wfile)
            return '[[[chat_stop]]]'
        FILES.append(state.wfile)
        if server:
            server.do_not_close = True
        return '[[[chat]]]'
    if state.command.startswith('/'):
        msg = state.command[1:]
        for wfile in tuple(FILES):
            if wfile is sys.stdout:
                R('print', string='[[[chat_message]]] ' + msg, wfile=wfile)
            else:
                try:
                    wfile.write(msg + '[[[br]]]')
                except BrokenPipeError:
                    FILES.remove(wfile)
        return f'[[[message_sent]]] {len(FILES)} [[[/message_sent]]]'
    return None

@R.handler('help', 'C2')
def _help(state):
    "help"
    state.help.append('  chat : [[[chat]]]')
    state.help.append('  / MSG: [[[/]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['chat_message'] = "Message received from chat:"
    state.translations['fr']['chat_message'] = "Message venant du tchat :"
    state.translations['en']['chat'] = "Displays futur chat messages"
    state.translations['fr']['chat'] = "Affiche les futurs messages du tchat"
    state.translations['en']['chat_stop'] = "No more display chat messages"
    state.translations['fr']['chat_stop'] = "N'affiche plus les messages du tchat"
    state.translations['en']['/'] = "Send the message on the chat"
    state.translations['fr']['/'] = "Envoyer le message sur le tchat"
    state.translations['en']['message_sent'] = "Message sent to"
    state.translations['fr']['message_sent'] = "Message envoyé à"
    state.translations['en']['/message_sent'] = "receivers."
    state.translations['fr']['/message_sent'] = "abonnés."

@R.handler('home_page')
def home_log(state):
    """Add the real time log display on home page"""
    state.items.append(
        {'column': 'C6', 'row': 'R0', 'html': 'CHAT', 'src': '/chat',
         'css': '<.> { font-family:monospace, monospace; white-space: pre; background: #8F8}'})

@R.handler('BEFORE_RELOAD')
def chat_reloaded(state):
    """Reload the web page if the chat module is reloaded"""
    if state.functionality == __name__:
        for wfile in FILES:
            if wfile is not sys.stdout:
                wfile.write('[[[RELOAD_HOME]]]')
