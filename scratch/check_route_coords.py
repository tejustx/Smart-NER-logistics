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
    time.sleep(1)

    send_and_wait(ws, {
        'id': 10,
        'method': 'Runtime.evaluate',
        'params': {'expression': 'performLogin("planner@nerlogistics.in", "Planner@123")', 'awaitPromise': True}
    })
    time.sleep(1.5)

    check_expr = '''
    (async () => {
        navigateToScreen("route-screen");
        await runUnifiedPlanAndAllocate("Tawang", "Itanagar");
        await new Promise(r => setTimeout(r, 1000));
        
        const map = appState.routeMap;
        const res = {
            center: map ? map.getCenter() : null,
            zoom: map ? map.getZoom() : null,
            pitch: map ? map.getPitch() : null,
            bearing: map ? map.getBearing() : null,
            layers: map && map.getStyle ? map.getStyle().layers.map(l => ({ id: l.id, type: l.type, paint: l.paint })) : [],
            routes: (appState.cachedRoutes || []).map(r => ({
                id: r.id,
                name: r.name,
                coordsLen: (r.path_coordinates || []).length,
                firstPt: (r.path_coordinates || [])[0],
                lastPt: (r.path_coordinates || [])[(r.path_coordinates || []).length - 1]
            }))
        };
        return JSON.stringify(res);
    })()
    '''
    res = send_and_wait(ws, {
        'id': 20,
        'method': 'Runtime.evaluate',
        'params': {'expression': check_expr, 'awaitPromise': True}
    })
    print("ROUTE DETAILS:", res.get('result', {}).get('result', {}).get('value'))
finally:
    proc.terminate()
