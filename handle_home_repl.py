"""
Add an REPL to the Web Home page
"""

from reactor import R

@R.handler('home_page')
def home_repl(state):
    """Add the INPUT evaluator on home page"""
    js_function = '''
function send_command(input) {
    var cmd = '/' + encodeURIComponent(input.value);
    var output = document.getElementById('output');
    if ( document.getElementById('profile').checked )
        cmd = '/PROFILE' + cmd;        
    output.setAttribute('src', cmd);
    load_data(output);
    setTimeout(function() { input.value = ''; }, 200);
}
'''
    html = '''[[[home_command]]]
        (<label><input id="profile" type="checkbox"> Profile</label>)
        <input style="width:100%" autofocus onchange="send_command(this)">
        [[[home_result]]]
        <div id="output" style="white-space: pre; font-family: monospace, monospace"></div>
        '''
    css = """DIV.C0 { display: flex; flex-direction: column; height: calc(100vh - 10px)}
    <.> { flex: 1; overflow: auto }
    """
    state.items.append({'column': 'C0', 'row': 'R1', 'html': html, 'js': js_function, 'css': css})

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['home_command'] = "Enter a command to evaluate"
    state.translations['fr']['home_command'] = "Saisissez une commande à évaluer"
    state.translations['en']['home_result'] = "The evaluation result:"
    state.translations['fr']['home_result'] = "Le résultat de l'évaluation :"

@R.handler('print', '0')
def add_reload_home(state):
    """Do reload home page on functionality reload or disable"""
    for i in ('[[[reloaded]]]', '[[[disabled]]]'):
        state.string = state.string.replace(i, i + '[[[RELOAD_HOME]]]')
