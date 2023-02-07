"""
Handle translation
"""

import collections
import re
from reactor import R

TRANSLATIONS = collections.defaultdict(dict)

def replace(group):
    """Replace by the translation"""
    key = group.group()[3:-3]
    return TRANSLATIONS.get(R.M.variables.get('LANG', 'en'), {}).get(key, key)

@R.handler('print', 'B')
def translate(args):
    """Translate"""
    args[1] = re.sub(r'\[\[\[([^]]*)]]]', replace, args[1])

@R.handler('INIT')
def _start(_args):
    R.M.variables['LANG'] = 'fr'
    R('translations', TRANSLATIONS)

@R.handler('help', 'S')
def print_help(args):
    """Help message"""
    args[1].append("[[[translations_help]]]")

@R.handler('RELOAD')
def _reload(_args):
    R('translations', TRANSLATIONS)

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['translations_help'] = "To see messages in french, type: LANG='fr'"
    args[1]['fr']['translations_help'] = "Pour voir les messages en anglais, tapez LANG='en'"

@R.handler('reply', 'A')
def _reply(args):
    """Translate the HTTP answer"""
    args[2] = re.sub(r'\[\[\[([^]]*)]]]', replace, args[2])
