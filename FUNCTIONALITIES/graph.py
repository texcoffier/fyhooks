"""
Generate call graph
"""

import traceback
import collections
import os
from typing import Dict, Tuple
from reactor import R

ARCS:Dict[Tuple[str,str], int] = collections.defaultdict(int)

def cleanup(filename):
    """Get the bare filename"""
    return filename.rsplit('/', 1)[-1].split('.')[0]

@R.handler('', 'A')
def _counter(state):
    """Increment the number of handler call"""
    origin = cleanup(traceback.extract_stack()[-3].filename)
    ARCS[origin, state.event] += 1

def get_svg():
    def node_id(txt):
        return txt.split('.')[-1]
    def nice(txt):
        return node_id(txt).replace('_', '\\n')
    fcties = '\n'.join(
        f'F{node_id(fcty)} [ label="{nice(fcty)}" color=blue shape=cylinder ]'
        for fcty in set(fct.__module__
                        for key, handlers in tuple(R.handlers.items())
                        for priority, index, fct in handlers
                        if not fct.__name__.startswith('_')))
    def description(key):
        lines = R.handler_descriptions.get(key, "").strip().split('\n')
        text = '<BR/>'.join(i.strip() for i in lines)
        return f'<<TABLE CELLSPACING="0"><TR><TD>{key}</TD></TR><TR><TD>{text}</TD></TR></TABLE>>'

    handlers = '\n'.join(
        f'H{key} [ label={description(key)} shape=none margin=0 ]'
        for key, _handlers in tuple(R.handlers.items())
        )
    arcs_in = '\n'.join(f'F{origin} -> H{goal} [label="{nbr}" penwidth=3 color=blue]'
                        for (origin, goal), nbr in ARCS.items()
                        )
    arcs_out = '\n'.join(f'H{key} -> F{node_id(fct.__module__)} [ label="{fct.__name__}"]'
                         for key, handlers in tuple(R.handlers.items())
                         for priority, index, fct in handlers
                         if not fct.__name__.startswith('_')
                        )
    dot = ('digraph {edge [fontname="Helvetica"]\n'
          + fcties + '\n'
          + handlers + '\n'
          + arcs_in + '\n'
          + arcs_out + '\n'
          + 'Fmain [ label="main" color=blue shape=cylinder ]' + '\n'
          + '}')
    with open("xxx.dot", "w", encoding='utf-8') as file:
        file.write(dot)
    os.system("dot -Tsvg xxx.dot >xxx.svg")
    with open("xxx.svg", "r", encoding='utf-8') as file:
        svg = file.read()
    return svg

@R.handler('eval')
def do_graph(state):
    """Generate the graph"""
    if state.command != 'pg':
        return None
    if not hasattr(state, 'server'):
        return get_svg()
    return state.server.svg

@R.handler('http')
def http(state):
    """Set the good HTTP header"""
    if state.server.path != '/pg':
        return None
    state.server.svg = get_svg()
    if '<svg' in state.server.svg:
        state.server.send_header('Content-Type', 'image/svg+xml; charset=UTF-8')
        return True
    state.server.svg = "[[[graphviz]]]"

@R.handler('help', 'C')
def _help(state):
    "help"
    state.help.append('  pg : [[[help_graph]]]')

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['help_graph'] = "Display call graph"
    state.translations['fr']['help_graph'] = "Affiche le graphe d'appel"
    state.translations['en']['graphviz'] = "To see the call graph: [[[BR]]][[[TT]]]apt install graphviz[[[/TT]]]"
    state.translations['fr']['graphviz'] = "Pour voir le graphe d'appel : [[[BR]]][[[TT]]]apt install graphviz[[[/TT]]]"

@R.handler('home_page')
def home_graph(state):
    """Add the application memory dump and reactor list on home page"""
    state.items.append(
        {'column': 'C2', 'row': 'R0', 'html': 'PM', 'src': '/pg',
         'css': '<.> svg { width: 20vw; height: auto }'})
