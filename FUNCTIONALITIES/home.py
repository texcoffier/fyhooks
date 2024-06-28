"""
Web Home page for the application.
It allows other functionalities to add block on the interface.
"""

import collections
from reactor import R

R.description('home_page', """Arguments: state.items
Append HTML elements to display, each element is defined by a dictionary:
{'column': str, 'row': str, 'html': str, 'src': str, 'css': str, 'js': str,
 'title': True, 'attributes': 'onclick="..." onmouseenter="..."'}
'column' and 'row' must be valid HTML class names
""")

@R.handler('http')
def http(state):
    """Set the good HTTP header"""
    # Should not be done as TRANSLATIONS because the path may be complex
    if state.server.path == '/index.html':
        state.server.send_header('Content-Type', 'text/html; charset=UTF-8')
        return True
    return None

@R.handler('eval')
def home(state):
    """Home page"""
    if state.command != 'index.html':
        return None
    items = []
    R('home_page', items=items)
    css = ['''
    BODY { margin: 0px; overflow: hidden }
    BODY > DIV { display: flex; }
    BODY > DIV > DIV { display: inline-block; overflow: auto; vertical-align: top }
    BODY > DIV > DIV > DIV { position: relative }
    BODY > DIV > DIV > DIV > H2 { margin: 2px }
    ''']
    js_function = ['''
    function load_data(div) {
        var url = div.getAttribute('src');
        if ( ! url )
            return;
        console.log("Reload " + url);
        var xhr = div.xhr;
        if (!xhr)
            xhr = new XMLHttpRequest();
        div.xhr = xhr;
        xhr.addEventListener('readystatechange',
            function(event) {
                if (event.target.readyState < 3)
                    return;
                if ( event.target.responseText.indexOf('[[[RELOAD_HOME]]]') != -1 ) {
                    window.location.reload();
                    }
                console.log("Receive " + event.target.responseText.length
                    + " bytes for " + url);
                if(event.target.responseText.substr(0, 1) == '<') {
                    div.innerHTML = event.target.responseText;
                    return;
                }
                var content = event.target.responseText
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/\\[\\[\\[/g, '<')
                    .replace(/\\]\\]\\]/g, '>')
                    .split('\\n')
                    ;
                div.innerHTML = '<H2>' + content[0] + '</H2>' + content.slice(1).join('\\n');
                })
        xhr.open("GET", url);
        xhr.send();
        }''']

    columns = collections.defaultdict(dict)
    for i, item in enumerate(items):
        column = item.get('column', '')
        row = item.get('row', '')
        css.append(item.get('css', '').replace('<.>', f'BODY > DIV > DIV.{column} > DIV.{row}'))
        js_function.append(item.get('js', ''))
        html = item.get('html', '')
        attributes = item.get('attributes', '')
        src = item.get('src', '')
        if src:
            html += f'<SCRIPT>load_data(document.getElementById("i{i}"))</SCRIPT>'
        columns[column][row] = (html, i, src, attributes)
    content = ['<STYLE>', ''.join(css), '</STYLE>',
               '<SCRIPT>', '\n'.join(js_function), '</SCRIPT>',
               '<DIV>'
               ]
    for column_class, cells in sorted(columns.items()):
        content.append(f'<DIV class="{column_class}">')
        for cell_class, (html, i, src, attributes) in sorted(cells.items()):
            content.append(f'<DIV class="{cell_class}" id="i{i}" src="{src}" {attributes}>')
            content.append(html)
            content.append('</DIV>')
        content.append('</DIV>')
    content.append('</DIV><DIV>')
    return ''.join(content)

@R.handler('START', 'N')
def start(_state):
    "help"
    R('print', string="[[[http_start]]] http://127.0.0.1:8888/index.html")
