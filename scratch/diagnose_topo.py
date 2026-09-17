import urllib.request, json, subprocess, time
import websocket

proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--remote-debugging-port=9222',
    '--remote-allow-origins=*',
    '--window-size=1600,1000',
    'http://localhost:8000/'
])
time.sleep(2)

def send_and_wait(ws, msg_dict, timeout=15):
    msg_id = msg_dict['id']
    ws.send(json.dumps(msg_dict))
    start = time.time()
    while time.time() - start < timeout:
        msg = ws.recv()
        resp = json.loads(msg)
        if resp.get('id') == msg_id:
            return resp
    raise TimeoutError(f"Timeout waiting for msg id {msg_id}")

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
    time.sleep(1)

    # Login
    send_and_wait(ws, {
        'id': 10,
        'method': 'Runtime.evaluate',
        'params': {'expression': 'performLogin("planner@nerlogistics.in", "Planner@123")', 'awaitPromise': True}
    })
    time.sleep(1.5)

    # Navigate to route screen and inspect map
    diag_expr = '''
    (async () => {
        navigateToScreen("route-screen");
        await new Promise(r => setTimeout(r, 1000));
        
        const map = appState.routeMap;
        const info1 = {
            hasMap: Boolean(map),
            isStyleLoaded: map ? map.isStyleLoaded() : false,
            layers: map && map.getStyle ? (map.getStyle().layers || []).map(l => l.id) : [],
            sources: map && map.getStyle ? Object.keys(map.getStyle().sources || {}) : []
        };
        
        // Now set topo
        setMapBasemapLayer("topo");
        await new Promise(r => setTimeout(r, 1500));
        
        const info2 = {
            hasMap: Boolean(map),
            isStyleLoaded: map ? map.isStyleLoaded() : false,
            layers: map && map.getStyle ? (map.getStyle().layers || []).map(l => l.id) : [],
            sources: map && map.getStyle ? Object.keys(map.getStyle().sources || {}) : [],
            cachedRoutesCount: (appState.cachedRoutes || []).length
        };
        
        return JSON.stringify({ before: info1, afterTopo: info2 });
    })()
    '''
    res = send_and_wait(ws, {
        'id': 20,
        'method': 'Runtime.evaluate',
        'params': {'expression': diag_expr, 'awaitPromise': True}
    })
    print("DIAGNOSTIC RESULT:", res.get('result', {}).get('result', {}).get('value'))
finally:
    proc.terminate()
