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
def translate(args):
    """Translate"""
    args[1] = re.sub(r'\[\[\[([^]]*)]]]', replace, str(args[1]))

@R.handler('PRESTART')
def _start(_args):
    R.M.variables['LANG'] = 'fr'
    R('translations', TRANSLATIONS)

@R.handler('help', 'S')
def print_help(args):
    """Help message"""
    args[1].append("[[[translations_help]]]")
@R.handler('help', 'C2')
def print_help2(args):
    "help"
    args[1].append('  pt : [[[dump_t]]]')

@R.handler('RELOAD')
def _reload(_args):
    R('translations', TRANSLATIONS)

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['translations_help'] = "To see messages in french, type: LANG='fr'"
    args[1]['fr']['translations_help'] = "Pour voir les messages en anglais, tapez LANG='en'"
    args[1]['en']['dump_t'] = "Translations dictionnary"
    args[1]['fr']['dump_t'] = "Les traductions des messages"

@R.handler('eval')
def do_dump(args):
    """If it is the dump command do it"""
    if args[1].strip() == 'pt':
        lines = ['[[[dump_t]]]\n']
        for lang, messages in TRANSLATIONS.items():
            lines.append(f'  ======== {lang} ========\n')
            for key, msg in sorted(messages.items()):
                lines.append(f'    {key:20} {msg.strip()[:40]}\n')
        return ''.join(lines)
    return None
