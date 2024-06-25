"""
Button box for Web Home page
It allows other functionalities to add buttons on the interface.
"""

from reactor import R

R.description("buttons", """Arguments: state.buttons
                            Called on home page initialization.
                            You append your buttons [command, label] to state.buttons""")

@R.handler('home_page')
def home_buttons(state):
    """Add a box containing button on the home page"""
    buttons = []
    R('buttons', buttons=buttons)
    content = []
    for url, label in buttons:
        content.append(f'<button onclick="do_reload(\'{url}\')">{label}</button> ')
    js_function = '''
    function do_reload(cmd) {
        var img = document.createElement('IMG');
        img.src = cmd;
        document.body.appendChild(img);
        setTimeout(function() { location.reload(); }, 100);
    }'''
    state.items.append(
        {'column': 'C0', 'row': 'R0', 'html': ''.join(content), 'js': js_function})
