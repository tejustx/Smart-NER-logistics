import urllib.request, json, subprocess, time

proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--remote-debugging-port=9222',
    'http://localhost:8000/'
])
time.sleep(2)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    import websocket
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    
    time.sleep(1)
    # Check if appState, Leaflet, MapLibre are initialized
    expr = '''
    JSON.stringify({
        hasL: typeof L !== "undefined",
        hasMapLibre: typeof maplibregl !== "undefined",
        appStateKeys: Object.keys(window.appState || {}),
        routeMap: Boolean(window.appState && window.appState.routeMap),
        routeCardsHTML: document.getElementById("routes-cards-container") ? document.getElementById("routes-cards-container").innerHTML.length : -1,
        activeScreen: window.appState ? window.appState.currentScreen : null
    })
    '''
    ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
    
    start = time.time()
    while time.time() - start < 3:
        try:
            ws.settimeout(1.0)
            msg = ws.recv()
            data = json.loads(msg)
            if data.get('method') == 'Runtime.consoleAPICalled':
                print('CONSOLE:', data['params']['type'], [a.get('value') for a in data['params']['args']])
            elif data.get('method') == 'Runtime.exceptionThrown':
                print('EXCEPTION:', data['params']['exceptionDetails']['text'], data['params']['exceptionDetails'].get('exception', {}).get('description'))
            elif data.get('id') == 2:
                print('PAGE STATE RESULT:', data.get('result', {}).get('result', {}).get('value'))
        except Exception as e:
            break
finally:
    proc.terminate()
