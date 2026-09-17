import math

# NER Real Highway Junction Coordinates
COORDS = {
    "Guwahati": [26.1445, 91.7362],
    "Mangaldai": [26.4350, 92.0350],
    "Dhekiajuli": [26.7000, 92.5000],
    "Tezpur": [26.6528, 92.7926],
    "Kaliabhomora": [26.6050, 92.8550],
    "Jagiroad": [26.1200, 92.2150],
    "Nagaon": [26.3452, 92.6840],
    "Kaziranga": [26.5800, 93.1700],
    "Numaligarh": [26.6200, 93.6000],
    "Gohpur": [26.9200, 93.1500],
    "Banderdewa": [27.0500, 93.4500],
    "Naharlagun": [27.1000, 93.7000],
    "Itanagar": [27.0844, 93.6053],
    "Bhalukpong": [27.0125, 92.6480],
    "Bomdila": [27.2645, 92.4225],
    "Dirang": [27.3582, 92.2415],
    "Sela_Pass": [27.5034, 92.1026],
    "Jang": [27.5750, 91.9800],
    "Tawang": [27.5861, 91.8594],
    "Nongpoh": [25.9000, 91.8800],
    "Umiam": [25.6600, 91.9100],
    "Shillong": [25.5788, 91.8933],
    "Jowai": [25.4450, 92.2050],
    "Khliehriat": [25.1800, 92.3600],
    "Silchar": [24.8170, 92.7950],
    "Vairengte": [24.5100, 92.7550],
    "Kolasib": [24.2250, 92.6800],
    "Aizawl": [23.7271, 92.7176],
    "Badarpur": [24.8900, 92.5700],
    "Karimganj": [24.8600, 92.3500],
    "Dharmanagar": [24.3700, 92.1600],
    "Kumarghat": [24.1600, 92.0300],
    "Ambassa": [23.9200, 91.8500],
    "Teliamura": [23.8350, 91.6300],
    "Agartala": [23.8315, 91.2868],
    "Lumding": [25.7500, 93.1700],
    "Dimapur": [25.9090, 93.7266],
    "Pagla_Pahar": [25.7900, 93.7700],
    "Kohima": [25.6751, 94.1086],
    "Senapati": [25.3500, 94.0200],
    "Kangpokpi": [25.1500, 93.9700],
    "Imphal": [24.8170, 93.9368],
    "Jiribam": [24.8000, 93.1200],
    "Noney": [24.8300, 93.6200],
    "Bongaigaon": [26.5000, 90.5500],
    "Siliguri": [26.7271, 88.3953],
    "Sevoke": [26.8900, 88.4700],
    "Rangpo": [27.1700, 88.5300],
    "Gangtok": [27.3314, 88.6138]
}

# Real physical road segments (bidirectional)
# Each segment can have intermediate points representing real mountain bends and highway curvature
ROAD_SEGMENTS = {
    # Tawang Axis (NH-13)
    ("Tawang", "Jang"): [[27.5861, 91.8594], [27.5800, 91.9100], [27.5750, 91.9800]],
    ("Jang", "Sela_Pass"): [[27.5750, 91.9800], [27.5400, 92.0400], [27.5034, 92.1026]],
    ("Sela_Pass", "Dirang"): [[27.5034, 92.1026], [27.4200, 92.1700], [27.3582, 92.2415]],
    ("Dirang", "Bomdila"): [[27.3582, 92.2415], [27.3100, 92.3300], [27.2645, 92.4225]],
    ("Bomdila", "Bhalukpong"): [[27.2645, 92.4225], [27.1500, 92.5300], [27.0125, 92.6480]],
    ("Bhalukpong", "Tezpur"): [[27.0125, 92.6480], [26.8200, 92.7100], [26.6528, 92.7926]],

    # Northern Assam Foothills / Floodplain (NH-15)
    ("Guwahati", "Mangaldai"): [[26.1445, 91.7362], [26.2800, 91.8900], [26.4350, 92.0350]],
    ("Mangaldai", "Dhekiajuli"): [[26.4350, 92.0350], [26.5600, 92.2700], [26.7000, 92.5000]],
    ("Dhekiajuli", "Tezpur"): [[26.7000, 92.5000], [26.6800, 92.6500], [26.6528, 92.7926]],
    ("Tezpur", "Gohpur"): [[26.6528, 92.7926], [26.7800, 92.9500], [26.9200, 93.1500]],
    ("Gohpur", "Banderdewa"): [[26.9200, 93.1500], [26.9900, 93.3000], [27.0500, 93.4500]],
    ("Banderdewa", "Itanagar"): [[27.0500, 93.4500], [27.0700, 93.5300], [27.0844, 93.6053]],

    # Southern 4-Lane Trunk Corridor (NH-27)
    ("Guwahati", "Jagiroad"): [[26.1445, 91.7362], [26.1300, 91.9800], [26.1200, 92.2150]],
    ("Jagiroad", "Nagaon"): [[26.1200, 92.2150], [26.2300, 92.4500], [26.3452, 92.6840]],
    ("Nagaon", "Kaliabhomora"): [[26.3452, 92.6840], [26.4800, 92.7700], [26.6050, 92.8550]],
    ("Kaliabhomora", "Tezpur"): [[26.6050, 92.8550], [26.6528, 92.7926]],
    ("Kaliabhomora", "Naharlagun"): [[26.6050, 92.8550], [26.7800, 93.2000], [26.9500, 93.5200], [27.1000, 93.7000]],
    ("Naharlagun", "Itanagar"): [[27.1000, 93.7000], [27.0844, 93.6053]],

    # East-West Assam Trunk to Upper Assam & Nagaland
    ("Nagaon", "Kaziranga"): [[26.3452, 92.6840], [26.4600, 92.9300], [26.5800, 93.1700]],
    ("Kaziranga", "Numaligarh"): [[26.5800, 93.1700], [26.6000, 93.3800], [26.6200, 93.6000]],
    ("Numaligarh", "Dimapur"): [[26.6200, 93.6000], [26.2600, 93.6600], [25.9090, 93.7266]],
    ("Nagaon", "Lumding"): [[26.3452, 92.6840], [26.0500, 92.9200], [25.7500, 93.1700]],
    ("Lumding", "Dimapur"): [[25.7500, 93.1700], [25.8300, 93.4500], [25.9090, 93.7266]],

    # Nagaland - Manipur Axis (NH-29 / NH-2)
    ("Dimapur", "Pagla_Pahar"): [[25.9090, 93.7266], [25.8500, 93.7500], [25.7900, 93.7700]],
    ("Pagla_Pahar", "Kohima"): [[25.7900, 93.7700], [25.7300, 93.9400], [25.6751, 94.1086]],
    ("Kohima", "Senapati"): [[25.6751, 94.1086], [25.5100, 94.0600], [25.3500, 94.0200]],
    ("Senapati", "Kangpokpi"): [[25.3500, 94.0200], [25.2500, 94.0000], [25.1500, 93.9700]],
    ("Kangpokpi", "Imphal"): [[25.1500, 93.9700], [24.9800, 93.9500], [24.8170, 93.9368]],

    # Meghalaya Axis (NH-6)
    ("Guwahati", "Nongpoh"): [[26.1445, 91.7362], [26.0200, 91.8100], [25.9000, 91.8800]],
    ("Nongpoh", "Umiam"): [[25.9000, 91.8800], [25.7800, 91.9000], [25.6600, 91.9100]],
    ("Umiam", "Shillong"): [[25.6600, 91.9100], [25.5788, 91.8933]],
    ("Shillong", "Jowai"): [[25.5788, 91.8933], [25.5100, 92.0500], [25.4450, 92.2050]],
    ("Jowai", "Khliehriat"): [[25.4450, 92.2050], [25.3100, 92.2800], [25.1800, 92.3600]],
    ("Khliehriat", "Badarpur"): [[25.1800, 92.3600], [25.0300, 92.4700], [24.8900, 92.5700]],
    ("Badarpur", "Silchar"): [[24.8900, 92.5700], [24.8500, 92.6800], [24.8170, 92.7950]],
    ("Lumding", "Silchar"): [[25.7500, 93.1700], [25.2800, 92.9800], [24.8170, 92.7950]],

    # Mizoram Axis (NH-306)
    ("Silchar", "Vairengte"): [[24.8170, 92.7950], [24.6600, 92.7750], [24.5100, 92.7550]],
    ("Vairengte", "Kolasib"): [[24.5100, 92.7550], [24.3600, 92.7150], [24.2250, 92.6800]],
    ("Kolasib", "Aizawl"): [[24.2250, 92.6800], [23.9700, 92.7000], [23.7271, 92.7176]],

    # Tripura Axis (NH-8)
    ("Badarpur", "Karimganj"): [[24.8900, 92.5700], [24.8600, 92.3500]],
    ("Karimganj", "Dharmanagar"): [[24.8600, 92.3500], [24.6100, 92.2500], [24.3700, 92.1600]],
    ("Dharmanagar", "Kumarghat"): [[24.3700, 92.1600], [24.2600, 92.0900], [24.1600, 92.0300]],
    ("Kumarghat", "Ambassa"): [[24.1600, 92.0300], [24.0400, 91.9400], [23.9200, 91.8500]],
    ("Ambassa", "Teliamura"): [[23.9200, 91.8500], [23.8800, 91.7400], [23.8350, 91.6300]],
    ("Teliamura", "Agartala"): [[23.8350, 91.6300], [23.8330, 91.4600], [23.8315, 91.2868]],

    # Manipur East-West Axis (NH-37)
    ("Silchar", "Jiribam"): [[24.8170, 92.7950], [24.8080, 92.9600], [24.8000, 93.1200]],
    ("Jiribam", "Noney"): [[24.8000, 93.1200], [24.8150, 93.3700], [24.8300, 93.6200]],
    ("Noney", "Imphal"): [[24.8300, 93.6200], [24.8230, 93.7800], [24.8170, 93.9368]],

    # Sikkim Axis (NH-27 / NH-10)
    ("Guwahati", "Bongaigaon"): [[26.1445, 91.7362], [26.3200, 91.1400], [26.5000, 90.5500]],
    ("Bongaigaon", "Siliguri"): [[26.5000, 90.5500], [26.6100, 89.4700], [26.7271, 88.3953]],
    ("Siliguri", "Sevoke"): [[26.7271, 88.3953], [26.8100, 88.4300], [26.8900, 88.4700]],
    ("Sevoke", "Rangpo"): [[26.8900, 88.4700], [27.0300, 88.5000], [27.1700, 88.5300]],
    ("Rangpo", "Gangtok"): [[27.1700, 88.5300], [27.2500, 88.5700], [27.3314, 88.6138]]
}

# Add bidirectional edges
graph = {}
for (u, v), pts in list(ROAD_SEGMENTS.items()):
    d = 0
    for i in range(len(pts)-1):
        d += math.dist(pts[i], pts[i+1]) * 111.0
    if u not in graph: graph[u] = []
    if v not in graph: graph[v] = []
    graph[u].append((v, d, pts))
    rev_pts = list(reversed(pts))
    graph[v].append((u, d, rev_pts))

print(f"Graph initialized with {len(graph)} nodes.")

import heapq
def find_path(start, goal, avoid_edges=None):
    avoid_edges = avoid_edges or set()
    queue = [(0, start, [start], [])]
    seen = {}
    while queue:
        cost, curr, path, coords = queue.pop(0)
        if curr == goal:
            return cost, path, coords
        if curr in seen and seen[curr] <= cost:
            continue
        seen[curr] = cost
        for neighbor, weight, seg_pts in graph.get(curr, []):
            edge = tuple(sorted([curr, neighbor]))
            if edge in avoid_edges:
                continue
            new_coords = coords + (seg_pts if not coords else seg_pts[1:])
            queue.append((cost + weight, neighbor, path + [neighbor], new_coords))
        queue.sort(key=lambda x: x[0])
    return None, None, None

# Test Tawang to Itanagar
cost1, path1, coords1 = find_path("Tawang", "Itanagar")
print("\n--- TAWANG -> ITANAGAR (ROUTE 1) ---")
print("Path:", " -> ".join(path1))
print(f"Distance: {cost1:.1f} km, Points count: {len(coords1)}")
print("Sample Coords:", coords1[:3], "...", coords1[-3:])

# Find distinct Route 2 by penalizing/avoiding primary bottleneck
avoid = {tuple(sorted([path1[len(path1)//2], path1[len(path1)//2 + 1]]))}
cost2, path2, coords2 = find_path("Tawang", "Itanagar", avoid_edges=avoid)
if not path2:
    # If no alternate highway edge, add minor realistic road curvature offset
    pass
print("\n--- TAWANG -> ITANAGAR (ROUTE 2) ---")
if path2:
    print("Path 2:", " -> ".join(path2))
    print(f"Distance 2: {cost2:.1f} km, Points count: {len(coords2)}")

# Test Dimapur to Agartala
cost_d_a, path_d_a, coords_d_a = find_path("Dimapur", "Agartala")
print("\n--- DIMAPUR -> AGARTALA ---")
print("Path:", " -> ".join(path_d_a))
print(f"Distance: {cost_d_a:.1f} km, Points count: {len(coords_d_a)}")
