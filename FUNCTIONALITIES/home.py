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

class Item:
    """A bloc of the HTML interface"""
    index = 0
    def __init__(self, item):
        for attribute in item:
            assert attribute in ('column', 'row', 'js', 'src', 'attributes', 'css', 'html')
        self.item = item
        self.i = self.index
        Item.index += 1
    def column(self):
        """Get HTML column name"""
        return self.item.get('column', '')
    def row(self):
        """Get HTML row name"""
        return self.item.get('row', '')
    def javascript(self):
        """Get Javascript helper function"""
        return self.item.get('js', '')
    def css(self):
        """Get CSS functionality style"""
        return self.item.get('css', '').replace('<.>',
            f'BODY > DIV > DIV.{self.column()} > DIV.{self.row()}')
    def html(self):
        """Get the HTML for the bloc"""
        src = self.item.get('src', '')
        attributes = self.item.get('attributes', '')
        content = f'<DIV class="{self.row()}" id="i{self.i}" src="{src}" {attributes}>'
        content += self.item.get('html', '')
        if src:
            content += f'<SCRIPT>load_data(document.getElementById("i{self.i}"))</SCRIPT>'
        content += '</DIV>'
        return content

@R.handler('eval')
def home(state):
    """Home page"""
    if state.command != 'index.html':
        return None
    items = []
    R('home_page', items=items)

    columns = collections.defaultdict(dict)
    items = [Item(item) for item in items]
    for item in items:
        columns[item.column()][item.row()] = item

    content = [
        '<STYLE>',
        'BODY { margin: 0px; overflow: hidden }',
        'BODY > DIV { display: flex; }',
        'BODY > DIV > DIV { display: inline-block; overflow: auto; vertical-align: top }',
        'BODY > DIV > DIV > DIV { position: relative }',
        'BODY > DIV > DIV > DIV > H2 { margin: 2px }',
        ''.join(item.css() for item in items),
        '</STYLE>',
        '<SCRIPT>', '''
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
        }''',
        '\n'.join(item.javascript() for item in items),
        '</SCRIPT>',
        '<DIV>'
        ]
    for column_class, cells in sorted(columns.items()):
        content.append(f'<DIV class="{column_class}">')
        for _cell_class, item in sorted(cells.items()):
            content.append(item.html())
        content.append('</DIV>')
    content.append('</DIV><DIV>')
    return ''.join(content)

@R.handler('START', 'N')
def start(_state):
    "help"
    R('print', string="[[[http_start]]] http://127.0.0.1:8888/index.html")
