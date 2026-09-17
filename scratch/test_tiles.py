import urllib.request

urls = {
    'carto_dark': 'https://basemaps.cartocdn.com/dark_all/6/28/50.png',
    'esri_dark': 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/6/28/50',
    'esri_topo': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/6/28/50',
    'esri_sat': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/6/28/50',
    'esri_street': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/6/28/50',
    'osm': 'https://tile.openstreetmap.org/6/28/50.png'
}

for name, u in urls.items():
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        res = urllib.request.urlopen(req, timeout=4)
        data = res.read()
        print(f"{name}: status={res.status}, bytes={len(data)}")
    except Exception as e:
        print(f"{name}: error={e}")
