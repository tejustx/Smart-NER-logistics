import subprocess
import time
import json
import urllib.request
import sys

# 1. Start server if not running
server_proc = None
try:
    urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1)
    print("Server already running on port 8000.")
except Exception:
    print("Starting uvicorn server...")
    server_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"
    ])
    for _ in range(15):
        time.sleep(1)
        try:
            urllib.request.urlopen("http://127.0.0.1:8000/", timeout=1)
            print("Server successfully bound to 8000.")
            break
        except Exception:
            pass

import tempfile
temp_dir = tempfile.mkdtemp()

# 2. Launch headless Edge with isolated user-data-dir
edge_proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless=new',
    f'--user-data-dir={temp_dir}',
    '--remote-debugging-port=9222',
    '--remote-allow-origins=*',
    'http://127.0.0.1:8000/'
])
time.sleep(3)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read().decode())
    app_tab = next(t for t in tabs if '8000' in t.get('url', ''))
    print("CONNECTED TO TAB:", app_tab.get('url'))
    import websocket
    ws = websocket.create_connection(app_tab['webSocketDebuggerUrl'])
    ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
    time.sleep(1)

    # Helper function to evaluate JS in the browser
    req_id = 10
    def eval_js(expression):
        global req_id
        req_id += 1
        cid = req_id
        wrapped_expr = f"JSON.stringify((() => {{ {expression} }})())"
        ws.send(json.dumps({
            'id': cid,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': wrapped_expr
            }
        }))
        start = time.time()
        while time.time() - start < 5:
            try:
                ws.settimeout(2.0)
                msg = ws.recv()
                data = json.loads(msg)
                print(f"MSG for cid={cid}: id={data.get('id')}, method={data.get('method')}")
                if data.get('id') == cid:
                    print(f"FOUND MATCHING DATA FOR {cid}:", json.dumps(data))
                    val = data.get('result', {}).get('result', {}).get('value')
                    if val is not None:
                        return json.loads(val)
                    return val
                elif 'error' in data or 'exceptionDetails' in data.get('result', {}):
                    print("CDP EVAL ERROR:", data)
            except Exception as e:
                print("RECV EXCEPTION:", e)
                break
        return None

    # Wait for page to initialize
    time.sleep(2)

    # Navigate to Route screen
    print("\nNavigating to Route Screen...")
    res = eval_js('''
        navigateToScreen("route-screen");
        return {
            activeScreen: window.appState.activeScreen,
            hasRouteMap: Boolean(window.appState.routeMap),
            activeLayer: window.appState.activeMapLayer || "dark"
        };
    ''')
    print("Screen state:", res)

    # Test Satellite Recon
    print("\nTesting switch to 'satellite'...")
    sat_res = eval_js('''
        setMapBasemapLayer("satellite");
        return {
            activeLayer: window.appState.activeMapLayer,
            routeBtnActive: document.querySelector('#route-map-layer-switcher .layer-btn[data-layer="satellite"]')?.classList.contains('active'),
            allActiveLayers: Array.from(document.querySelectorAll('.map-layer-switcher .layer-btn.active')).map(b => b.getAttribute('data-layer'))
        };
    ''')
    print("Satellite switch result:", sat_res)
    assert sat_res['activeLayer'] == 'satellite', "activeLayer should be satellite"
    assert sat_res['routeBtnActive'] is True, "Route button satellite should be active"

    # Test Topo Terrain
    print("\nTesting switch to 'topo'...")
    topo_res = eval_js('''
        setMapBasemapLayer("topo");
        return {
            activeLayer: window.appState.activeMapLayer,
            routeBtnActive: document.querySelector('#route-map-layer-switcher .layer-btn[data-layer="topo"]')?.classList.contains('active')
        };
    ''')
    print("Topo switch result:", topo_res)
    assert topo_res['activeLayer'] == 'topo', "activeLayer should be topo"
    assert topo_res['routeBtnActive'] is True, "Route button topo should be active"

    # Test Vector Light
    print("\nTesting switch to 'light'...")
    light_res = eval_js('''
        setMapBasemapLayer("light");
        return {
            activeLayer: window.appState.activeMapLayer,
            routeBtnActive: document.querySelector('#route-map-layer-switcher .layer-btn[data-layer="light"]')?.classList.contains('active')
        };
    ''')
    print("Light switch result:", light_res)
    assert light_res['activeLayer'] == 'light', "activeLayer should be light"

    # Test Vector Dark
    print("\nTesting switch to 'dark'...")
    dark_res = eval_js('''
        setMapBasemapLayer("dark");
        return {
            activeLayer: window.appState.activeMapLayer,
            routeBtnActive: document.querySelector('#route-map-layer-switcher .layer-btn[data-layer="dark"]')?.classList.contains('active')
        };
    ''')
    print("Dark switch result:", dark_res)
    assert dark_res['activeLayer'] == 'dark', "activeLayer should be dark"

    # Test Government Screen
    print("\nNavigating to Government Oversight Screen...")
    gov_res = eval_js('''
        navigateToScreen("gov-screen");
        setMapBasemapLayer("satellite");
        return {
            activeScreen: window.appState.activeScreen,
            hasGovMap: Boolean(window.appState.govMap),
            activeLayer: window.appState.activeMapLayer,
            govBtnActive: document.querySelector('#gov-map-layer-switcher .layer-btn[data-layer="satellite"]')?.classList.contains('active')
        };
    ''')
    print("Gov screen result:", gov_res)
    assert gov_res['activeLayer'] == 'satellite', "Gov activeLayer should be satellite"
    assert gov_res['govBtnActive'] is True, "Gov button satellite should be active"
    assert gov_res['hasGovMap'] is True, "Gov map should be initialized"

    print("\n>>> ALL BASEMAP SWITCHER VERIFICATION TESTS PASSED SUCCESSFULLY! <<<")

finally:
    try:
        edge_proc.terminate()
    except Exception:
        pass
    if server_proc:
        try:
            server_proc.terminate()
        except Exception:
            pass
