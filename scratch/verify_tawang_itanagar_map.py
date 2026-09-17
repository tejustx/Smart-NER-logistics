import urllib.request, json, subprocess, time, base64, os
import websocket

ARTIFACT_DIR = r"C:\Users\tejas\.gemini\antigravity-ide\brain\eb4d8ea1-cab3-4c8f-8c8e-e48f9c594c61"

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

    # 1. Login
    send_and_wait(ws, {
        'id': 10,
        'method': 'Runtime.evaluate',
        'params': {'expression': 'performLogin("planner@nerlogistics.in", "Planner@123")', 'awaitPromise': True}
    })
    time.sleep(1.5)

    # 2. Go to route screen, select Tawang -> Itanagar, and switch to Topo
    topo_expr = '''
    (async () => {
        navigateToScreen("route-screen");
        appState.selectedOrigin = "Tawang";
        appState.selectedDestination = "Itanagar";
        await runUnifiedPlanAndAllocate("Tawang", "Itanagar");
        if (typeof setMapBasemapLayer === "function") {
            setMapBasemapLayer("topo");
        }
        return "Topo and Tawang-Itanagar ready";
    })()
    '''
    send_and_wait(ws, {
        'id': 20,
        'method': 'Runtime.evaluate',
        'params': {'expression': topo_expr, 'awaitPromise': True}
    })
    time.sleep(4)

    # Capture Topo screenshot
    res_snap = send_and_wait(ws, {
        'id': 30,
        'method': 'Page.captureScreenshot',
        'params': {'format': 'png'}
    })
    img_data = base64.b64decode(res_snap['result']['data'])
    topo_path = os.path.join(ARTIFACT_DIR, "real_highway_tawang_itanagar_topo.png")
    with open(topo_path, "wb") as f:
        f.write(img_data)
    print("Saved topo screenshot to:", topo_path)

    # 3. Test Dimapur -> Agartala on Topo as well
    dim_aga_expr = '''
    (async () => {
        appState.selectedOrigin = "Dimapur";
        appState.selectedDestination = "Agartala";
        await runUnifiedPlanAndAllocate("Dimapur", "Agartala");
        return "Dimapur-Agartala evaluated";
    })()
    '''
    send_and_wait(ws, {
        'id': 40,
        'method': 'Runtime.evaluate',
        'params': {'expression': dim_aga_expr, 'awaitPromise': True}
    })
    time.sleep(4)

    res_snap2 = send_and_wait(ws, {
        'id': 50,
        'method': 'Page.captureScreenshot',
        'params': {'format': 'png'}
    })
    img_data2 = base64.b64decode(res_snap2['result']['data'])
    dim_path = os.path.join(ARTIFACT_DIR, "real_highway_dimapur_agartala_topo.png")
    with open(dim_path, "wb") as f:
        f.write(img_data2)
    print("Saved Dimapur-Agartala screenshot to:", dim_path)

finally:
    proc.terminate()
    print("Edge headless closed.")
