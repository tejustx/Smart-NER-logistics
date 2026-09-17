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

def send_and_wait(ws, msg_dict, timeout=20):
    msg_id = msg_dict['id']
    ws.send(json.dumps(msg_dict))
    start = time.time()
    while time.time() - start < timeout:
        msg = ws.recv()
        resp = json.loads(msg)
        if resp.get('id') == msg_id:
            return resp
    raise TimeoutError(f"Timeout waiting for msg id {msg_id}")

def capture(ws, req_id, filename):
    time.sleep(3)
    res_snap = send_and_wait(ws, {
        'id': req_id,
        'method': 'Page.captureScreenshot',
        'params': {'format': 'png'}
    })
    img_data = base64.b64decode(res_snap['result']['data'])
    out_path = os.path.join(ARTIFACT_DIR, filename)
    with open(out_path, "wb") as f:
        f.write(img_data)
    print(f"Captured {filename} ({len(img_data)} bytes)")

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

    # 2. Go to route screen, select Tawang -> Itanagar on Satellite Recon
    eval_script = '''
    (async () => {
        navigateToScreen("route-screen");
        const origSel = document.getElementById("route-quick-origin");
        const destSel = document.getElementById("route-quick-dest");
        if (origSel) origSel.value = "Tawang";
        if (destSel) destSel.value = "Itanagar";
        setMapBasemapLayer("satellite");
        await runUnifiedPlanAndAllocate("Tawang", "Itanagar");
        return "Tawang Itanagar Satellite ready";
    })()
    '''
    send_and_wait(ws, {
        'id': 20,
        'method': 'Runtime.evaluate',
        'params': {'expression': eval_script, 'awaitPromise': True}
    })
    capture(ws, 30, "tawang_itanagar_satellite_verified.png")

    # 3. Switch to Topo Terrain
    switch_topo = '''
    (async () => {
        setMapBasemapLayer("topo");
        return "Topo switched";
    })()
    '''
    send_and_wait(ws, {
        'id': 40,
        'method': 'Runtime.evaluate',
        'params': {'expression': switch_topo, 'awaitPromise': True}
    })
    capture(ws, 50, "tawang_itanagar_topo_verified.png")

    # 4. Switch to Vector Dark
    switch_dark = '''
    (async () => {
        setMapBasemapLayer("dark");
        return "Dark switched";
    })()
    '''
    send_and_wait(ws, {
        'id': 60,
        'method': 'Runtime.evaluate',
        'params': {'expression': switch_dark, 'awaitPromise': True}
    })
    capture(ws, 70, "tawang_itanagar_dark_verified.png")

    # 5. Dimapur -> Agartala on Satellite
    dim_aga = '''
    (async () => {
        const origSel = document.getElementById("route-quick-origin");
        const destSel = document.getElementById("route-quick-dest");
        if (origSel) origSel.value = "Dimapur";
        if (destSel) destSel.value = "Agartala";
        setMapBasemapLayer("satellite");
        await runUnifiedPlanAndAllocate("Dimapur", "Agartala");
        return "Dimapur Agartala ready";
    })()
    '''
    send_and_wait(ws, {
        'id': 80,
        'method': 'Runtime.evaluate',
        'params': {'expression': dim_aga, 'awaitPromise': True}
    })
    capture(ws, 90, "dimapur_agartala_satellite_verified.png")

finally:
    proc.terminate()
    print("Edge headless closed.")
