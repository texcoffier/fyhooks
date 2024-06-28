"""
Add a reload button on home page blocks
"""

from reactor import R

@R.handler('home_page', "Z")
def home_reload(state):
    """Manage click on each bloc with an 'src' attribute"""
    for item in state.items:
        if 'src' in item:
            item['attributes'] = (
                ' onclick="load_data(this)"'
                + ' ondblclick="window.open(this.getAttribute(\'src\'))"'
            )

@R.handler('home_page')
def home_dump(state):
    """Add help on home page"""
    state.items.append(
        {'column': 'C0', 'row': 'A0', 'html': '[[[home_click]]]',
         'css': '<.> { background: #888; color: #FFF}'})

@R.handler('translations')
def _translations(state):
    "Translations"
    state.translations['en']['home_click'] = (
        "Click on a bloc to reload it. Double click to open it in a tab")
    state.translations['fr']['home_click'] = (
        "Cliquez vous recharger le block. Double cliquez pour ouvrir dans un onglet.")
