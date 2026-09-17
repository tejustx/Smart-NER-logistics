import urllib.request, socket

socket.setdefaulttimeout(5)
services = [
    ('dark', 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/7/54/98'),
    ('light', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/7/54/98'),
    ('satellite', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/7/54/98'),
    ('topo', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/7/54/98')
]

for name, url in services:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print(f"{name}: SUCCESS ({len(res.read())} bytes)")
    except Exception as e:
        print(f"{name}: FAILED ({e})")
