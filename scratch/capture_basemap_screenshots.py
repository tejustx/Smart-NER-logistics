import subprocess
import time
import json
import urllib.request
import base64
import tempfile
import os

ARTIFACT_DIR = r"C:\Users\tejas\.gemini\antigravity-ide\brain\eb4d8ea1-cab3-4c8f-8c8e-e48f9c594c61"
temp_dir = tempfile.mkdtemp()

edge_proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless=new',
    '--window-size=1440,900',
    f'--user-data-dir={temp_dir}',
    '--remote-debugging-port=9223',
    '--remote-allow-origins=*',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    '--use-gl=angle',
    '--use-angle=d3d11',
    'http://127.0.0.1:8000/'
])
time.sleep(3)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9223/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    import websocket
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
    time.sleep(2)

    req_id = 100
    def send_cdp(method, params=None):
        global req_id
        req_id += 1
        cid = req_id
        ws.send(json.dumps({'id': cid, 'method': method, 'params': params or {}}))
        start = time.time()
        while time.time() - start < 6:
            try:
                ws.settimeout(2.0)
                msg = ws.recv()
                data = json.loads(msg)
                if data.get('id') == cid:
                    return data.get('result')
            except Exception:
                break
        return None

    # Login and navigate to Route screen with Satellite basemap
    send_cdp('Runtime.evaluate', {
        'expression': 'instantLogin("planner");',
        'awaitPromise': True
    })
    time.sleep(2)

    send_cdp('Runtime.evaluate', {
        'expression': 'navigateToScreen("route-screen"); setMapBasemapLayer("satellite");'
    })
    time.sleep(4) # allow tiles to load
    shot1 = send_cdp('Page.captureScreenshot', {'format': 'png'})
    if shot1 and 'data' in shot1:
        out1 = os.path.join(ARTIFACT_DIR, 'arcgis_satellite_recon.png')
        with open(out1, 'wb') as f:
            f.write(base64.b64decode(shot1['data']))
        print("Saved:", out1)

    # Switch to Topo
    send_cdp('Runtime.evaluate', {
        'expression': 'setMapBasemapLayer("topo");'
    })
    time.sleep(3) # allow tiles to load
    shot2 = send_cdp('Page.captureScreenshot', {'format': 'png'})
    if shot2 and 'data' in shot2:
        out2 = os.path.join(ARTIFACT_DIR, 'arcgis_topo_terrain.png')
        with open(out2, 'wb') as f:
            f.write(base64.b64decode(shot2['data']))
        print("Saved:", out2)

finally:
    try:
        edge_proc.terminate()
    except Exception:
        pass
