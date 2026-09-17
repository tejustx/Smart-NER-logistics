import subprocess
import time
import json
import urllib.request
import tempfile
import websocket

temp_dir = tempfile.mkdtemp()
edge_proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless=new',
    f'--user-data-dir={temp_dir}',
    '--remote-debugging-port=9224',
    '--remote-allow-origins=*',
    'http://127.0.0.1:8000/'
])
time.sleep(3)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9224/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    time.sleep(1)

    req_id = 10
    def eval_js(expr):
        global req_id
        req_id += 1
        cid = req_id
        ws.send(json.dumps({'id': cid, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'awaitPromise': True, 'returnByValue': True}}))
        start = time.time()
        while time.time() - start < 5:
            msg = ws.recv()
            d = json.loads(msg)
            if d.get('method') == 'Runtime.consoleAPICalled':
                print("BROWSER CONSOLE:", d['params']['type'], [a.get('value') for a in d['params']['args']])
            elif d.get('method') == 'Runtime.exceptionThrown':
                print("BROWSER EXCEPTION:", d['params']['exceptionDetails']['text'], d['params']['exceptionDetails'].get('exception', {}).get('description'))
            elif d.get('id') == cid:
                if 'exceptionDetails' in d.get('result', {}):
                    print("EVAL EXCEPTION:", d['result']['exceptionDetails']['text'], d['result']['exceptionDetails'].get('exception', {}).get('description'))
                return d.get('result', {}).get('result', {}).get('value')
        return None

    print("Logging in...")
    eval_js('instantLogin("planner");')
    time.sleep(2)
    eval_js('navigateToScreen("route-screen");')
    time.sleep(3)

    layers_initial = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS INITIAL (DARK):", layers_initial)

    print("Switching to Satellite Recon...")
    eval_js('setMapBasemapLayer("satellite");')
    time.sleep(2)

    layers_sat = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS AFTER SATELLITE SWITCH:", layers_sat)

    print("Switching to Topo Terrain...")
    eval_js('setMapBasemapLayer("topo");')
    time.sleep(2)

    layers_topo = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS AFTER TOPO SWITCH:", layers_topo)

    print("Switching to Vector Light (ArcGIS World Street Map)...")
    eval_js('setMapBasemapLayer("light");')
    time.sleep(2)

    layers_light = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS AFTER LIGHT SWITCH:", layers_light)

    print("Switching back to Vector Dark (ArcGIS Dark Gray Canvas)...")
    eval_js('setMapBasemapLayer("dark");')
    time.sleep(2)

    layers_dark = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS AFTER DARK SWITCH:", layers_dark)

    print("Changing corridor to Dimapur -> Agartala on Satellite...")
    eval_js('''
        setMapBasemapLayer("satellite");
        document.getElementById("route-quick-origin").value = "Dimapur";
        document.getElementById("route-quick-dest").value = "Agartala";
        onQuickCorridorChange();
    ''')
    time.sleep(3)

    layers_corridor = eval_js('JSON.stringify(appState.routeMap.getStyle().layers.map(l => l.id))')
    print("LAYERS AFTER CORRIDOR CHANGE:", layers_corridor)

    routes_info = eval_js('''
        JSON.stringify({
            cachedRoutesCount: (appState.cachedRoutes || []).length,
            cachedRouteIds: (appState.cachedRoutes || []).map(r => r.id),
            hasPathCoords: (appState.cachedRoutes || []).map(r => Boolean(r.path_coordinates && r.path_coordinates.length))
        })
    ''')
    print("ROUTES INFO:", routes_info)

finally:
    edge_proc.terminate()
