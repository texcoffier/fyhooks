from reactor import R

@R.handler('http')
def http(state):
    """Set the good HTTP header"""
    # XXX: should be done has TRANSLATIONS
    if state.server.path == '/index.html':
        state.server.send_header('Content-Type', 'text/html; charset=UTF-8')
        return True
    return None

@R.handler('eval')
def home(state):
    """Home page"""
    if state.command == 'index.html':
        return r'''
<style>
    BODY { box-sizing: border-box; margin: 0px; }
    IFRAME { box-sizing: border-box; white-space: nowrap }
    BODY > DIV { display: inline-block; width: 25vw; height: 100% }
    BODY > DIV > DIV:nth-child(1) { height: 70% }
    BODY > DIV > DIV:nth-child(2) { height: 20% }
    BODY > DIV > DIV:nth-child(3) { height: 10% }
</style>
<script>
function do_reload(cmd) {
    var img = document.createElement('IMG');
    img.src = cmd;
    document.body.appendChild(img);
    setTimeout(function() { location.reload(); }, 100);
}
function send_command(input) {
    var cmd = '/' + input.value;
    var iframe = input;
    while(iframe.tagName != 'IFRAME')
        iframe = iframe.nextSibling;
    if ( document.getElementById('profile').checked )
        cmd = '/PROFILE' + cmd;        
    iframe.src = cmd;
    setTimeout(function() {
        var iframe = document.getElementById('pm');
        var src = iframe.src;
        iframe.src = src;
        }, 200);
}
</script>
<div><div>
        <button onclick="do_reload('/r')">[[[home_reload_modules]]]</button>
        <button onclick="do_reload('/LANG=\'fr\'')">FR</button>
        <button onclick="do_reload('/LANG=\'en\'')">EN</button>
        <p>
        [[[home_command]]] (<label><input id="profile" type="checkbox"> Profile</label>)
        <input style="width:100%" onchange="send_command(this)">
        [[[home_result]]]
        <iframe width="100%" height="80%"></iframe>
    </div>
    <div><iframe src="/h" width="100%" height="100%"></iframe></div>
    <div><iframe id="pm" src="/pm" width="100%" height="100%"></iframe></div>
</div><div><iframe src="/pr" width="100%" height="100%"></iframe>
</div><div><iframe src="/l" width="100%" height="100%"></iframe>
</div><div><iframe src="/pt" width="100%" height="100%"></iframe></div>
        '''
    return None


@R.handler('START', 'N')
def _start(_state):
    "help"
    R('print', string="[[[http_start]]] http://127.0.0.1:8888/index.html")

@R.handler('translations')
def translations(state):
    "Translations"
    state.translations['en']['home_reload_modules'] = "Reload Python modules"
    state.translations['fr']['home_reload_modules'] = "Recharge les module Python"
    state.translations['en']['home_command'] = "Enter a command to evaluate"
    state.translations['fr']['home_command'] = "Saisissez une commande à évaluer"
    state.translations['en']['home_result'] = "The evaluation result:"
    state.translations['fr']['home_result'] = "Le résultat de l'évaluation :"
