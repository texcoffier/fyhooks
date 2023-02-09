"""
Handle translation
"""

from typing import Dict
import collections
import re
from reactor import R

TRANSLATIONS:Dict[str,Dict[str,str]] = collections.defaultdict(dict)

def replace(group):
    """Replace by the translation"""
    key = group.group()[3:-3]
    return TRANSLATIONS.get(R.M.variables.get('LANG', 'en'), {}).get(key, key)

@R.handler('print', 'B')
def translate(state):
    """Translate"""
    state.string = re.sub(r'\[\[\[([^]]*)]]]', replace, str(state.string))

@R.handler('PRESTART')
def _start(_state):
    R.M.variables['LANG'] = 'fr'
    R('translations', translations=TRANSLATIONS)

@R.handler('help', 'S')
def print_help(state):
    """Help message"""
    state.help.append("[[[translations_help]]]")
@R.handler('help', 'C2')
def print_help2(state):
    "help"
    state.help.append('  pt : [[[dump_t]]]')

@R.handler('RELOAD')
def _reload(_state):
    R('translations', translations=TRANSLATIONS)

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['translations_help'] = "To see messages in french, type: LANG='fr'"
    state.translations['fr']['translations_help'] = "Pour voir les messages en anglais, tapez LANG='en'"
    state.translations['en']['dump_t'] = "Translations dictionnary"
    state.translations['fr']['dump_t'] = "Les traductions des messages"

@R.handler('eval')
def do_dump(state):
    """If it is the dump command do it"""
    if state.command == 'pt':
        lines = ['[[[dump_t]]]\n']
        for lang, messages in TRANSLATIONS.items():
            lines.append(f'======== {lang} ========\n')
            for key, msg in sorted(messages.items()):
                lines.append(f'{key:17} {msg.strip()}\n')
        return ''.join(lines)
    return None

@R.handler('buttons')
def language(state):
    """Add reload button"""
    for lang in TRANSLATIONS:
        state.buttons.append((f"/LANG=\\'{lang}\\'", lang))
