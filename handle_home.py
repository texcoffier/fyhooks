"""
Web Home page for the application
"""

from reactor import R

@R.handler('http')
def http(state):
    """Set the good HTTP header"""
    # Should not be done has TRANSLATIONS because the path may be complex
    if state.server.path == '/index.html':
        state.server.send_header('Content-Type', 'text/html; charset=UTF-8')
        return True
    return None

@R.handler('eval')
def home(state):
    """Home page"""
    if state.command != 'index.html':
        return None
    content = ['''
<style>
    BODY { box-sizing: border-box; margin: 0px; overflow: hidden }
    BODY, INPUT, BUTTON { font-family: monospace,monospace; font-size: 0.7vw; }
    BODY > DIV { display: inline-block; height: 100%; white-space: pre;
                 vertical-align: top; overflow: auto}
    BODY > DIV > DIV { overflow: auto; white-space: pre;}
    DIV#output { white-space: pre;}
    BODY > DIV > DIV:nth-child(1) { height: 15%; background: #EFF;  white-space:normal }
    BODY > DIV > DIV:nth-child(2) { height: 45%; background: #F8F8F8 }
    BODY > DIV > DIV:nth-child(3) { height: 25%; background: #FEF }
    BODY > DIV > DIV:nth-child(4) { height: 15%; background: #FFE }
    BODY > DIV:nth-child(1) { width: 36vw; overflow: hidden; white-space:normal }
    BODY > DIV:nth-child(2) { width: 22vw; background: #FEE }
    BODY > DIV:nth-child(3) { width: 19vw; background: #EFE }
    BODY > DIV:nth-child(4) { width: 23vw; background: #EEF }
</style>
<script>
function do_reload(cmd) {
    var img = document.createElement('IMG');
    img.src = cmd;
    document.body.appendChild(img);
    setTimeout(function() { location.reload(); }, 100);
}
function send_command(input) {
    var cmd = '/' + encodeURIComponent(input.value);
    var output = document.getElementById('output');
    if ( document.getElementById('profile').checked )
        cmd = '/PROFILE' + cmd;        
    output.setAttribute('src', cmd);
    load_data(output);
    setTimeout(function() { document.getElementById('pm'); }, 200);
}
function load_data(div) {
    var url = div.getAttribute('src');
    if ( ! url )
        return;
    var xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange',
        function(event) {
            div.innerHTML = event.target.responseText.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            })
    xhr.open("GET", url);
    xhr.send();
}
</script>
<div><div>''']
    buttons = []
    R('buttons', buttons=buttons)
    for url, label in buttons:
        content.append(f'<button onclick="do_reload(\'{url}\')">{label}</button> ')
    content.append('''
        <p>
        [[[home_command]]] (<label><input id="profile" type="checkbox"> Profile</label>)
        <input style="width:100%" onchange="send_command(this)">
        [[[home_result]]]
        </div><div id="output" style="background:#F8F8F8"></div><div src="/h"></div><div id="pm" src="/pm"></div>
    </div><div src="/pr"></div><div src="/l"></div><div src="/pt"></div>
<script>
var divs = document.getElementsByTagName('DIV');
for(var div of divs)
    load_data(div);
</script>
        ''')
    return ''.join(content)

@R.handler('START', 'N')
def _start(_state):
    "help"
    R('print', string="[[[http_start]]] http://127.0.0.1:8888/index.html")

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['home_command'] = "Enter a command to evaluate"
    state.translations['fr']['home_command'] = "Saisissez une commande à évaluer"
    state.translations['en']['home_result'] = "The evaluation result:"
    state.translations['fr']['home_result'] = "Le résultat de l'évaluation :"
