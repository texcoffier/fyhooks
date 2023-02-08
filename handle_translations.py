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
    args[1] = re.sub(r'\[\[\[([^]]*)]]]', replace, str(args[1]))

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

@R.handler('informations')
def _informations(args):
    """Dump some informations"""
    for lang, messages in TRANSLATIONS.items():
        args[1].append(f'  ======== {lang} ========\n')
        for key, msg in sorted(messages.items()):
            args[1].append(f'    {key:20} {msg.strip()[:40]}\n')
