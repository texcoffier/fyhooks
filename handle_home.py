from reactor import R

@R.handler('http')
def http(args):
    if args[1] == 'index.html':
        args[2].send_header('Content-Type', 'text/html; charset=UTF-8')
        return True

@R.handler('eval')
def home(args):
    """Home page"""
    if args[1].strip() == 'index.html':
        return r'''
<style>
    BODY { box-sizing: border-box; margin: 0px }
    PRE { margin: 0px }
    IFRAME { }
    TABLE { width: 100%; height: 100%; position: absolute; top: 0px; bottom: 0px }
    TABLE TR { height: 20% }
    TD { width: 20% }
    INPUT { width: 100% }
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
    iframe.src = cmd;
}
</script>
<table>
<tr>
<td>
    <button onclick="do_reload('/r')">[[[home_reload_modules]]]</button>
    <button onclick="do_reload('/LANG=\'fr\'')">FR</button>
    <button onclick="do_reload('/LANG=\'en\'')">EN</button>
    <p>
    [[[home_command]]]
    <input onchange="send_command(this)">
    [[[home_result]]]
    <iframe width="100%" height="100px"></iframe>

<td rowspan="5"><iframe src="/ph" width="100%" height="100%"></iframe></td>
<td rowspan="5"><iframe src="/pr" width="100%" height="100%"></iframe></td>
<td rowspan="5"><iframe src="/l" width="100%" height="100%"></iframe></td>
<td rowspan="5"><iframe src="/pt" width="100%" height="100%"></iframe></td>
</tr>
<tr>
<td rowspan="1"><iframe src="/h" width="100%" height="100%"></iframe></td>
</tr>
<tr>
<td rowspan="1"><iframe src="/pm" width="100%" height="100%"></iframe></td>
</tr>
</table>
        '''
    return None


@R.handler('help', 'T')
def print_help(args):
    "help"
    args[1].append('[[[http_start]]] http://127.0.0.1:8888/index.html')

@R.handler('translations')
def translations(args):
    "Translations"
    args[1]['en']['home_reload_modules'] = "Reload Python modules"
    args[1]['fr']['home_reload_modules'] = "Recharge les module Python"
    args[1]['en']['home_command'] = "Enter a command to evaluate"
    args[1]['fr']['home_command'] = "Saisissez une commande à évaluer"
    args[1]['en']['home_result'] = "The evaluation result:"
    args[1]['fr']['home_result'] = "Le résultat de l'évaluation :"

