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
    '--remote-debugging-port=9225',
    '--remote-allow-origins=*',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    '--use-gl=angle',
    '--use-angle=d3d11',
    'http://127.0.0.1:8000/'
])
time.sleep(3)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9225/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    import websocket
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
    time.sleep(1)

    req_id = 100
    def send_cdp(method, params=None):
        global req_id
        req_id += 1
        cid = req_id
        ws.send(json.dumps({'id': cid, 'method': method, 'params': params or {}}))
        start = time.time()
        while time.time() - start < 8:
            try:
                ws.settimeout(2.0)
                msg = ws.recv()
                data = json.loads(msg)
                if data.get('id') == cid:
                    return data.get('result')
            except Exception:
                break
        return None

    # 1. Login and go to route screen
    send_cdp('Runtime.evaluate', {'expression': 'instantLogin("planner");', 'awaitPromise': True})
    time.sleep(2)
    send_cdp('Runtime.evaluate', {'expression': 'navigateToScreen("route-screen");'})
    time.sleep(4)

    # 2. Capture clean Dark Mode (ArcGIS Dark Gray Canvas - No API Key error!)
    shot_dark = send_cdp('Page.captureScreenshot', {'format': 'png'})
    if shot_dark and 'data' in shot_dark:
        out = os.path.join(ARTIFACT_DIR, 'arcgis_dark_canvas.png')
        with open(out, 'wb') as f:
            f.write(base64.b64decode(shot_dark['data']))
        print("Saved:", out)

    # 3. Switch to Dimapur -> Agartala corridor on Satellite Recon
    send_cdp('Runtime.evaluate', {
        'expression': '''
            setMapBasemapLayer("satellite");
            document.getElementById("route-quick-origin").value = "Dimapur";
            document.getElementById("route-quick-dest").value = "Agartala";
            onQuickCorridorChange();
        '''
    })
    time.sleep(5)
    shot_sat_dim = send_cdp('Page.captureScreenshot', {'format': 'png'})
    if shot_sat_dim and 'data' in shot_sat_dim:
        out = os.path.join(ARTIFACT_DIR, 'arcgis_satellite_dimapur_agartala.png')
        with open(out, 'wb') as f:
            f.write(base64.b64decode(shot_sat_dim['data']))
        print("Saved:", out)

    # 4. Switch to Light Mode (ArcGIS World Street Map - No API Key error!)
    send_cdp('Runtime.evaluate', {'expression': 'setMapBasemapLayer("light");'})
    time.sleep(4)
    shot_light = send_cdp('Page.captureScreenshot', {'format': 'png'})
    if shot_light and 'data' in shot_light:
        out = os.path.join(ARTIFACT_DIR, 'arcgis_light_street.png')
        with open(out, 'wb') as f:
            f.write(base64.b64decode(shot_light['data']))
        print("Saved:", out)

finally:
    edge_proc.terminate()
