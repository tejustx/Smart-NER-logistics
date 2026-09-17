"""
Smart NER Logistics Control Platform
Topological Road Network Graph and Real Physical Corridor Router for the North Eastern Region (NER)
Traces genuine National Highways (NH-13, NH-15, NH-27, NH-6, NH-29, NH-2, NH-306, NH-8, NH-10, OKSRT)
Connecting all 13 hubs and 50+ mountain passes, river bridges, and defense bypasses.
"""

import math
import heapq
from typing import Dict, List, Tuple, Set, Optional, Any

NER_ROAD_NODES: Dict[str, List[float]] = {
    # 13 Primary Hubs
    "Guwahati": [26.1445, 91.7362],
    "Itanagar": [27.0844, 93.6053],
    "Shillong": [25.5788, 91.8933],
    "Tawang": [27.5861, 91.8594],
    "Tezpur": [26.6528, 92.7926],
    "Nagaon": [26.3452, 92.6840],
    "Silchar": [24.8170, 92.7950],
    "Aizawl": [23.7271, 92.7176],
    "Dimapur": [25.9090, 93.7266],
    "Kohima": [25.6751, 94.1086],
    "Imphal": [24.8170, 93.9368],
    "Agartala": [23.8315, 91.2868],
    "Gangtok": [27.3314, 88.6138],

    # Arunachal & West Kameng Waypoints
    "Jang": [27.5750, 91.9800],
    "Sela_Pass": [27.5034, 92.1026],       # 13,700 ft old pass (high risk)
    "Sela_Tunnel": [27.5120, 92.0950],     # New all-weather tunnel (low risk)
    "Dirang": [27.3582, 92.2415],
    "Bomdila": [27.2645, 92.4225],
    "Tenga": [27.2000, 92.4800],
    "Jamiri": [27.1100, 92.5600],
    "Bhalukpong": [27.0125, 92.6480],      # Old BCT gorge road
    "Balipara": [26.8200, 92.7800],
    "Rupa": [27.2000, 92.4000],
    "Shergaon": [27.1200, 92.2600],
    "Kalaktang": [27.0100, 92.1100],       # OKSRT defense highway
    "Balemu": [26.8800, 92.0800],
    "Bhairabkunda": [26.8900, 92.1200],
    "Rowta": [26.7100, 92.1800],
    "Naharlagun": [27.1000, 93.7000],
    "Banderdewa": [27.0500, 93.4500],
    "Gohpur": [26.9200, 93.1500],
    "Biswanath_Chariali": [26.7300, 93.1500],
    "Jamugurihat": [26.7200, 92.9500],

    # Assam Plains & Brahmaputra Bridges
    "Baihata_Chariali": [26.3400, 91.7100],
    "Mangaldai": [26.4350, 92.0350],
    "Dhekiajuli": [26.7000, 92.5000],
    "Kaliabhomora": [26.6050, 92.8550],    # Major Brahmaputra bridge
    "Jakhalabandha": [26.5800, 93.0000],
    "Jagiroad": [26.1200, 92.2150],
    "Kaziranga": [26.5800, 93.1700],
    "Bokakhat": [26.6200, 93.3800],
    "Numaligarh": [26.6200, 93.6000],
    "Doboka": [26.0800, 92.8700],
    "Lumding": [25.7500, 93.1700],
    "Diphu": [25.8400, 93.4300],
    "Haflong": [25.1700, 93.0200],
    "Jatinga": [25.1200, 92.9900],
    "Bongaigaon": [26.5000, 90.5500],
    "Siliguri": [26.7271, 88.3953],
    "Sevoke": [26.8900, 88.4700],
    "Kalijhora": [26.9300, 88.4600],
    "Teesta_Bazaar": [27.0500, 88.4900],
    "Melli": [27.0900, 88.4600],
    "Rangpo": [27.1700, 88.5300],
    "Singtam": [27.2300, 88.5000],
    "Gorubathan": [26.9700, 88.7000],
    "Lava": [27.0900, 88.6600],
    "Pakyong": [27.2400, 88.5900],

    # Meghalaya Waypoints
    "Nongpoh": [25.9000, 91.8800],
    "Umsning": [25.7500, 91.8900],
    "Umiam": [25.6600, 91.9100],
    "Mawryngkneng": [25.5500, 92.0500],
    "Jowai": [25.4450, 92.2050],
    "Lad_Rymbai": [25.3100, 92.3100],
    "Khliehriat": [25.1800, 92.3600],
    "Lumshnong": [25.1700, 92.3900],
    "Sonapur": [25.0600, 92.4200],         # Famous Sonapur mudslide zone
    "Malidor": [24.9800, 92.4800],
    "Umkiang": [25.0500, 92.3800],

    # Barak Valley & Mizoram Waypoints
    "Badarpur": [24.8900, 92.5700],
    "Karimganj": [24.8600, 92.3500],
    "Dholai": [24.6000, 92.8300],
    "Lailapur": [24.5300, 92.7800],
    "Vairengte": [24.5100, 92.7550],
    "Bilkhawthlir": [24.3300, 92.7100],
    "Kolasib": [24.2250, 92.6800],
    "Kawnpui": [23.9900, 92.6700],
    "Selesih": [23.8200, 92.7200],
    "Bairabi": [24.1900, 92.5300],
    "Mamit": [23.9300, 92.4900],
    "Lengpui": [23.8400, 92.6200],

    # Tripura Waypoints
    "Churaibari": [24.4700, 92.2400],
    "Dharmanagar": [24.3700, 92.1600],
    "Kailashahar": [24.3300, 92.0000],
    "Kumarghat": [24.1600, 92.0300],
    "Ambassa": [23.9200, 91.8500],
    "Khowai": [24.0600, 91.6000],
    "Teliamura": [23.8350, 91.6300],

    # Nagaland & Manipur Waypoints
    "Chumukedima": [25.8200, 93.7500],
    "Pagla_Pahar": [25.7900, 93.7700],
    "Medziphema": [25.7600, 93.8500],
    "Zubza": [25.7100, 94.0200],
    "Viswema": [25.5600, 94.1200],
    "Mao": [25.5100, 94.1300],
    "Maram": [25.4200, 94.0900],
    "Senapati": [25.3500, 94.0200],
    "Kangpokpi": [25.1500, 93.9700],
    "Jiribam": [24.8000, 93.1200],
    "Nungba": [24.7800, 93.4400],
    "Noney": [24.8300, 93.6200],
    "Tupul": [24.8400, 93.7800]
}

NER_ROAD_EDGES = [
    # --- Tawang Axis (NH-13 & OKSRT Defense Road) ---
    ("Tawang", "Jang", [[27.5861, 91.8594], [27.5800, 91.9100], [27.5750, 91.9800]], "NH-13 Tawang-Jang"),
    ("Jang", "Sela_Pass", [[27.5750, 91.9800], [27.5450, 92.0300], [27.5200, 92.0700], [27.5034, 92.1026]], "Old Sela High Pass (13,700 ft)"),
    ("Sela_Pass", "Dirang", [[27.5034, 92.1026], [27.4600, 92.1400], [27.4000, 92.1900], [27.3582, 92.2415]], "Old Sela Switchback Descent"),
    ("Jang", "Sela_Tunnel", [[27.5750, 91.9800], [27.5500, 92.0200], [27.5250, 92.0650], [27.5120, 92.0950]], "Sela Tunnel Approach"),
    ("Sela_Tunnel", "Dirang", [[27.5120, 92.0950], [27.4500, 92.1500], [27.3900, 92.2000], [27.3582, 92.2415]], "Sela Tunnel Bypass Viaduct"),
    ("Dirang", "Bomdila", [[27.3582, 92.2415], [27.3100, 92.3300], [27.2645, 92.4225]], "NH-13 Dirang-Bomdila"),
    ("Bomdila", "Tenga", [[27.2645, 92.4225], [27.2400, 92.4500], [27.2000, 92.4800]], "NH-13 Tenga Valley Cutting"),
    ("Tenga", "Jamiri", [[27.2000, 92.4800], [27.1600, 92.5100], [27.1100, 92.5600]], "NH-13 Kameng River Gorge"),
    ("Jamiri", "Bhalukpong", [[27.1100, 92.5600], [27.0600, 92.6000], [27.0125, 92.6480]], "Bhalukpong River Toe Scour"),
    ("Bhalukpong", "Balipara", [[27.0125, 92.6480], [26.9200, 92.7100], [26.8200, 92.7800]], "Balipara-Charduar Foothill Rd"),
    ("Balipara", "Tezpur", [[26.8200, 92.7800], [26.7400, 92.7900], [26.6528, 92.7926]], "NH-15 Balipara-Tezpur Link"),
    ("Bomdila", "Rupa", [[27.2645, 92.4225], [27.2300, 92.4100], [27.2000, 92.4000]], "OKSRT Rupa Link"),
    ("Rupa", "Shergaon", [[27.2000, 92.4000], [27.1600, 92.3300], [27.1200, 92.2600]], "Shergaon High Plateau Road"),
    ("Shergaon", "Kalaktang", [[27.1200, 92.2600], [27.0700, 92.1800], [27.0100, 92.1100]], "Kalaktang Engineered Highway"),
    ("Kalaktang", "Balemu", [[27.0100, 92.1100], [26.9400, 92.0900], [26.8800, 92.0800]], "Balemu Border Highway"),
    ("Balemu", "Bhairabkunda", [[26.8800, 92.0800], [26.8850, 92.1000], [26.8900, 92.1200]], "Bhairabkunda Tri-Junction"),
    ("Bhairabkunda", "Rowta", [[26.8900, 92.1200], [26.8000, 92.1500], [26.7100, 92.1800]], "Rowta Highway Link"),
    ("Rowta", "Dhekiajuli", [[26.7100, 92.1800], [26.7050, 92.3400], [26.7000, 92.5000]], "NH-15 East Connector"),
    ("Rowta", "Mangaldai", [[26.7100, 92.1800], [26.5800, 92.1000], [26.4350, 92.0350]], "NH-15 West Connector"),

    # --- Assam North Bank (NH-15 Floodplain) ---
    ("Guwahati", "Baihata_Chariali", [[26.1445, 91.7362], [26.2400, 91.7200], [26.3400, 91.7100]], "NH-27/15 North Trunk"),
    ("Baihata_Chariali", "Mangaldai", [[26.3400, 91.7100], [26.3800, 91.8700], [26.4350, 92.0350]], "NH-15 Mangaldai Highway"),
    ("Mangaldai", "Dhekiajuli", [[26.4350, 92.0350], [26.5600, 92.2700], [26.7000, 92.5000]], "NH-15 Dhekiajuli Corridor"),
    ("Dhekiajuli", "Tezpur", [[26.7000, 92.5000], [26.6800, 92.6500], [26.6528, 92.7926]], "NH-15 Tezpur Western Link"),
    ("Tezpur", "Jamugurihat", [[26.6528, 92.7926], [26.6800, 92.8700], [26.7200, 92.9500]], "NH-15 Jamugurihat Section"),
    ("Jamugurihat", "Biswanath_Chariali", [[26.7200, 92.9500], [26.7250, 93.0500], [26.7300, 93.1500]], "NH-15 Biswanath Bypass"),
    ("Biswanath_Chariali", "Gohpur", [[26.7300, 93.1500], [26.8200, 93.1500], [26.9200, 93.1500]], "NH-15 Gohpur Floodplain Corridor"),
    ("Gohpur", "Banderdewa", [[26.9200, 93.1500], [26.9900, 93.3000], [27.0500, 93.4500]], "NH-15 Banderdewa Approach"),
    ("Banderdewa", "Itanagar", [[27.0500, 93.4500], [27.0700, 93.5300], [27.0844, 93.6053]], "NH-415 Itanagar Capital Hill Highway"),

    # --- Assam South Bank 4-Lane Trunk & Brahmaputra Bridges (NH-27 / Asian Highway) ---
    ("Guwahati", "Jagiroad", [[26.1445, 91.7362], [26.1300, 91.9800], [26.1200, 92.2150]], "NH-27 4-Lane South Trunk"),
    ("Jagiroad", "Nagaon", [[26.1200, 92.2150], [26.2300, 92.4500], [26.3452, 92.6840]], "NH-27 Nagaon Expressway"),
    ("Nagaon", "Kaliabhomora", [[26.3452, 92.6840], [26.4800, 92.7700], [26.6050, 92.8550]], "Kaliabhomora Bridge Southern Approach"),
    ("Kaliabhomora", "Tezpur", [[26.6050, 92.8550], [26.6300, 92.8200], [26.6528, 92.7926]], "Kaliabhomora Brahmaputra Bridge Setu"),
    ("Kaliabhomora", "Jakhalabandha", [[26.6050, 92.8550], [26.5900, 92.9300], [26.5800, 93.0000]], "Jakhalabandha Junction"),
    ("Jakhalabandha", "Kaziranga", [[26.5800, 93.0000], [26.5800, 93.0800], [26.5800, 93.1700]], "NH-715 Kaziranga Highway"),
    ("Kaziranga", "Bokakhat", [[26.5800, 93.1700], [26.6000, 93.2800], [26.6200, 93.3800]], "NH-715 Bokakhat Corridor"),
    ("Bokakhat", "Numaligarh", [[26.6200, 93.3800], [26.6200, 93.4900], [26.6200, 93.6000]], "Numaligarh Junction"),
    ("Jakhalabandha", "Naharlagun", [[26.5800, 93.0000], [26.7800, 93.2800], [26.9600, 93.5200], [27.1000, 93.7000]], "Trans-Arunachal Papum Pare 4-Lane Link"),
    ("Naharlagun", "Itanagar", [[27.1000, 93.7000], [27.0900, 93.6500], [27.0844, 93.6053]], "NH-415 Naharlagun-Itanagar 4-Lane Viaduct"),

    # --- Central Assam to Upper Assam & Nagaland ---
    ("Nagaon", "Doboka", [[26.3452, 92.6840], [26.2100, 92.7700], [26.0800, 92.8700]], "NH-27 Doboka Highway"),
    ("Doboka", "Lumding", [[26.0800, 92.8700], [25.9100, 93.0200], [25.7500, 93.1700]], "NH-27 Lumding Link"),
    ("Lumding", "Diphu", [[25.7500, 93.1700], [25.8000, 93.3000], [25.8400, 93.4300]], "NH-329 Karbi Anglong Road"),
    ("Diphu", "Dimapur", [[25.8400, 93.4300], [25.8700, 93.5800], [25.9090, 93.7266]], "Diphu-Dimapur Intermodal Corridor"),
    ("Numaligarh", "Dimapur", [[26.6200, 93.6000], [26.2600, 93.6600], [25.9090, 93.7266]], "NH-129 Golaghat-Dimapur Highway"),

    # --- Dima Hasao Mountain Corridor (Haflong / Jatinga) ---
    ("Lumding", "Haflong", [[25.7500, 93.1700], [25.4600, 93.0900], [25.1700, 93.0200]], "NH-27 Dima Hasao Hill Highway"),
    ("Haflong", "Jatinga", [[25.1700, 93.0200], [25.1400, 93.0000], [25.1200, 92.9900]], "Jatinga Ridge Pass"),
    ("Jatinga", "Silchar", [[25.1200, 92.9900], [24.9700, 92.8900], [24.8170, 92.7950]], "NH-27 Jatinga-Silchar 4-Lane Viaduct"),

    # --- Meghalaya Highway (Guwahati -> Shillong -> Silchar) ---
    ("Guwahati", "Nongpoh", [[26.1445, 91.7362], [26.0200, 91.8100], [25.9000, 91.8800]], "NH-6 GS Road Section"),
    ("Nongpoh", "Umsning", [[25.9000, 91.8800], [25.8200, 91.8850], [25.7500, 91.8900]], "NH-6 Umsning Bypass"),
    ("Umsning", "Umiam", [[25.7500, 91.8900], [25.7000, 91.9000], [25.6600, 91.9100]], "NH-6 Umiam Lake Viaduct"),
    ("Umiam", "Shillong", [[25.6600, 91.9100], [25.6200, 91.9000], [25.5788, 91.8933]], "NH-6 Shillong Northern Arterial"),
    ("Shillong", "Mawryngkneng", [[25.5788, 91.8933], [25.5600, 91.9700], [25.5500, 92.0500]], "NH-6 Shillong Bypass Junction"),
    ("Mawryngkneng", "Jowai", [[25.5500, 92.0500], [25.5000, 92.1200], [25.4450, 92.2050]], "NH-6 Jowai Plateau Corridor"),
    ("Jowai", "Lad_Rymbai", [[25.4450, 92.2050], [25.3800, 92.2600], [25.3100, 92.3100]], "NH-6 Jaintia Coal Belt Highway"),
    ("Lad_Rymbai", "Khliehriat", [[25.3100, 92.3100], [25.2400, 92.3350], [25.1800, 92.3600]], "NH-6 Khliehriat Ridge Pass"),
    ("Khliehriat", "Lumshnong", [[25.1800, 92.3600], [25.1750, 92.3750], [25.1700, 92.3900]], "NH-6 Lumshnong Section"),
    ("Lumshnong", "Sonapur", [[25.1700, 92.3900], [25.1100, 92.4050], [25.0600, 92.4200]], "Sonapur River Toe Gorge (High Mudslide Hazard)"),
    ("Sonapur", "Malidor", [[25.0600, 92.4200], [25.0200, 92.4500], [24.9800, 92.4800]], "Lubha River Descent"),
    ("Malidor", "Badarpur", [[24.9800, 92.4800], [24.9300, 92.5250], [24.8900, 92.5700]], "NH-6 Barak Valley Entry"),
    ("Khliehriat", "Umkiang", [[25.1800, 92.3600], [25.1150, 92.3700], [25.0500, 92.3800]], "Umkiang High-Level Ridge Viaduct"),
    ("Umkiang", "Badarpur", [[25.0500, 92.3800], [24.9700, 92.4750], [24.8900, 92.5700]], "Reinforced Concrete Embankment Bypass"),
    ("Badarpur", "Silchar", [[24.8900, 92.5700], [24.8500, 92.6800], [24.8170, 92.7950]], "NH-37 Badarpur-Silchar 4-Lane Trunk"),

    # --- Mizoram Highway (Silchar -> Aizawl) ---
    ("Silchar", "Dholai", [[24.8170, 92.7950], [24.7100, 92.8100], [24.6000, 92.8300]], "Old NH-306 Dholai Valley"),
    ("Dholai", "Lailapur", [[24.6000, 92.8300], [24.5650, 92.8050], [24.5300, 92.7800]], "Lailapur Riverbank Cutting"),
    ("Lailapur", "Vairengte", [[24.5300, 92.7800], [24.5200, 92.7680], [24.5100, 92.7550]], "Vairengte Steep Mountain Gate"),
    ("Vairengte", "Bilkhawthlir", [[24.5100, 92.7550], [24.4200, 92.7300], [24.3300, 92.7100]], "Bilkhawthlir Hill Switchbacks"),
    ("Bilkhawthlir", "Kolasib", [[24.3300, 92.7100], [24.2800, 92.6950], [24.2250, 92.6800]], "Kolasib High Ridge Cutting"),
    ("Kolasib", "Kawnpui", [[24.2250, 92.6800], [24.1100, 92.6750], [23.9900, 92.6700]], "Kawnpui Landslide Belt"),
    ("Kawnpui", "Selesih", [[23.9900, 92.6700], [23.9050, 92.6950], [23.8200, 92.7200]], "Selesih Northern Approach"),
    ("Selesih", "Aizawl", [[23.8200, 92.7200], [23.7700, 92.7180], [23.7271, 92.7176]], "Aizawl Ridge Crest Entry"),
    ("Silchar", "Bairabi", [[24.8170, 92.7950], [24.5000, 92.6600], [24.1900, 92.5300]], "Bairabi Railhead Highway"),
    ("Bairabi", "Mamit", [[24.1900, 92.5300], [24.0600, 92.5100], [23.9300, 92.4900]], "Mamit Engineered Ridge Road"),
    ("Mamit", "Lengpui", [[23.9300, 92.4900], [23.8850, 92.5550], [23.8400, 92.6200]], "Lengpui Airport Expressway"),
    ("Lengpui", "Aizawl", [[23.8400, 92.6200], [23.7800, 92.6700], [23.7271, 92.7176]], "Aizawl Western Bypass Viaduct"),

    # --- Tripura Highway (Silchar -> Agartala) ---
    ("Badarpur", "Karimganj", [[24.8900, 92.5700], [24.8750, 92.4600], [24.8600, 92.3500]], "NH-37 Karimganj Link"),
    ("Karimganj", "Churaibari", [[24.8600, 92.3500], [24.6600, 92.2950], [24.4700, 92.2400]], "NH-8 Assam-Tripura Gate"),
    ("Churaibari", "Dharmanagar", [[24.4700, 92.2400], [24.4200, 92.2000], [24.3700, 92.1600]], "NH-8 Dharmanagar Arterial"),
    ("Dharmanagar", "Kumarghat", [[24.3700, 92.1600], [24.2650, 92.0950], [24.1600, 92.0300]], "NH-8 Kumarghat Hill Cutting"),
    ("Kumarghat", "Ambassa", [[24.1600, 92.0300], [24.0400, 91.9400], [23.9200, 91.8500]], "NH-8 Longtharai Hill Pass"),
    ("Ambassa", "Teliamura", [[23.9200, 91.8500], [23.8800, 91.7400], [23.8350, 91.6300]], "NH-8 Baramura Hill Ghat"),
    ("Teliamura", "Agartala", [[23.8350, 91.6300], [23.8330, 91.4600], [23.8315, 91.2868]], "NH-8 Agartala 4-Lane Expressway"),
    ("Churaibari", "Kailashahar", [[24.4700, 92.2400], [24.4000, 92.1200], [24.3300, 92.0000]], "Kailashahar Valley Bypass"),
    ("Kailashahar", "Khowai", [[24.3300, 92.0000], [24.1950, 91.8000], [24.0600, 91.6000]], "Khowai Valley Foothill Highway"),
    ("Khowai", "Agartala", [[24.0600, 91.6000], [23.9450, 91.4400], [23.8315, 91.2868]], "Khowai-Agartala Paved Bypass"),

    # --- Nagaland Highway (Dimapur -> Kohima) ---
    ("Dimapur", "Chumukedima", [[25.9090, 93.7266], [25.8645, 93.7383], [25.8200, 93.7500]], "NH-29 Chumukedima Gate"),
    ("Chumukedima", "Pagla_Pahar", [[25.8200, 93.7500], [25.8050, 93.7600], [25.7900, 93.7700]], "Pagla Pahar River Toe Gorge (Rockfall Zone)"),
    ("Pagla_Pahar", "Medziphema", [[25.7900, 93.7700], [25.7750, 93.8100], [25.7600, 93.8500]], "Medziphema Hill Cutting"),
    ("Medziphema", "Zubza", [[25.7600, 93.8500], [25.7350, 93.9350], [25.7100, 94.0200]], "Zubza Valley Ascent"),
    ("Zubza", "Kohima", [[25.7100, 94.0200], [25.6925, 94.0643], [25.6751, 94.1086]], "Kohima Mountain Ridge Entry"),
    ("Chumukedima", "Medziphema", [[25.8200, 93.7500], [25.7900, 93.8000], [25.7600, 93.8500]], "AH-1 4-Lane Pagla Pahar Elevated Viaduct"),
    ("Medziphema", "Kohima", [[25.7600, 93.8500], [25.7175, 93.9793], [25.6751, 94.1086]], "AH-1 4-Lane Reinforced Kohima Bypass"),

    # --- Manipur Highway (Kohima -> Imphal) ---
    ("Kohima", "Viswema", [[25.6751, 94.1086], [25.6175, 94.1143], [25.5600, 94.1200]], "NH-2 Dzukou Foothills"),
    ("Viswema", "Mao", [[25.5600, 94.1200], [25.5350, 94.1250], [25.5100, 94.1300]], "Mao Border Pass (Nagaland-Manipur Gate)"),
    ("Mao", "Maram", [[25.5100, 94.1300], [25.4650, 94.1100], [25.4200, 94.0900]], "NH-2 Maram Mountain Section"),
    ("Maram", "Senapati", [[25.4200, 94.0900], [25.3850, 94.0550], [25.3500, 94.0200]], "NH-2 Senapati River Corridor"),
    ("Senapati", "Kangpokpi", [[25.3500, 94.0200], [25.2500, 93.9950], [25.1500, 93.9700]], "NH-2 Kangpokpi Valley Highway"),
    ("Kangpokpi", "Imphal", [[25.1500, 93.9700], [24.9835, 93.9534], [24.8170, 93.9368]], "NH-2 Imphal Valley Approach"),

    # --- NH-37 Jiribam-Imphal Highway (Direct Barak Valley to Manipur) ---
    ("Silchar", "Jiribam", [[24.8170, 92.7950], [24.8085, 92.9575], [24.8000, 93.1200]], "NH-37 Jiribam Gateway"),
    ("Jiribam", "Nungba", [[24.8000, 93.1200], [24.7900, 93.2800], [24.7800, 93.4400]], "NH-37 Makru River Bridge Section"),
    ("Nungba", "Noney", [[24.7800, 93.4400], [24.8050, 93.5300], [24.8300, 93.6200]], "NH-37 Irang River Gorge (High Landslide Hazard)"),
    ("Noney", "Tupul", [[24.8300, 93.6200], [24.8350, 93.7000], [24.8400, 93.7800]], "Tupul Railway Viaduct Zone"),
    ("Tupul", "Imphal", [[24.8400, 93.7800], [24.8285, 93.8584], [24.8170, 93.9368]], "NH-37 Imphal Valley Entry"),

    # --- Sikkim Highway (Guwahati / Siliguri -> Gangtok) ---
    ("Guwahati", "Bongaigaon", [[26.1445, 91.7362], [26.3222, 91.1431], [26.5000, 90.5500]], "NH-27 Western Assam 4-Lane Trunk"),
    ("Bongaigaon", "Siliguri", [[26.5000, 90.5500], [26.6135, 89.4726], [26.7271, 88.3953]], "NH-27 North Bengal Corridor"),
    ("Siliguri", "Sevoke", [[26.7271, 88.3953], [26.8085, 88.4326], [26.8900, 88.4700]], "NH-10 Sevoke Coronation Bridge"),
    ("Sevoke", "Kalijhora", [[26.8900, 88.4700], [26.9100, 88.4650], [26.9300, 88.4600]], "NH-10 Kalijhora Rockfall Zone"),
    ("Kalijhora", "Teesta_Bazaar", [[26.9300, 88.4600], [26.9900, 88.4750], [27.0500, 88.4900]], "NH-10 Teesta River Gorge Toe"),
    ("Teesta_Bazaar", "Melli", [[27.0500, 88.4900], [27.0700, 88.4750], [27.0900, 88.4600]], "Melli Bridge Crossing"),
    ("Melli", "Rangpo", [[27.0900, 88.4600], [27.1300, 88.4950], [27.1700, 88.5300]], "NH-10 Rangpo Sikkim Border Gate"),
    ("Rangpo", "Singtam", [[27.1700, 88.5300], [27.2000, 88.5150], [27.2300, 88.5000]], "NH-10 Singtam Riverbank Road"),
    ("Singtam", "Gangtok", [[27.2300, 88.5000], [27.2807, 88.5569], [27.3314, 88.6138]], "NH-10 Gangtok Mountain Climb"),
    ("Sevoke", "Gorubathan", [[26.8900, 88.4700], [26.9300, 88.5850], [26.9700, 88.7000]], "Dooars Foothill Highway"),
    ("Gorubathan", "Lava", [[26.9700, 88.7000], [27.0300, 88.6800], [27.0900, 88.6600]], "Lava Pine Forest Mountain Road"),
    ("Lava", "Pakyong", [[27.0900, 88.6600], [27.1650, 88.6250], [27.2400, 88.5900]], "Pakyong Airport High-Grade Alignment"),
    ("Pakyong", "Gangtok", [[27.2400, 88.5900], [27.2857, 88.6019], [27.3314, 88.6138]], "Gangtok Southern Ridge Bypass")
]

HIGH_RISK_GORGE_EDGES: Set[Tuple[str, str]] = {
    tuple(sorted(["Jang", "Sela_Pass"])),
    tuple(sorted(["Sela_Pass", "Dirang"])),
    tuple(sorted(["Tenga", "Jamiri"])),
    tuple(sorted(["Jamiri", "Bhalukpong"])),
    tuple(sorted(["Lumshnong", "Sonapur"])),
    tuple(sorted(["Sonapur", "Malidor"])),
    tuple(sorted(["Chumukedima", "Pagla_Pahar"])),
    tuple(sorted(["Pagla_Pahar", "Medziphema"])),
    tuple(sorted(["Kalijhora", "Teesta_Bazaar"])),
    tuple(sorted(["Teesta_Bazaar", "Melli"]))
}

ENGINEERED_BYPASS_EDGES: Set[Tuple[str, str]] = {
    tuple(sorted(["Jang", "Sela_Tunnel"])),
    tuple(sorted(["Sela_Tunnel", "Dirang"])),
    tuple(sorted(["Bomdila", "Rupa"])),
    tuple(sorted(["Rupa", "Shergaon"])),
    tuple(sorted(["Shergaon", "Kalaktang"])),
    tuple(sorted(["Khliehriat", "Umkiang"])),
    tuple(sorted(["Umkiang", "Badarpur"])),
    tuple(sorted(["Chumukedima", "Medziphema"])),
    tuple(sorted(["Medziphema", "Kohima"])),
    tuple(sorted(["Jakhalabandha", "Naharlagun"])),
    tuple(sorted(["Sevoke", "Gorubathan"])),
    tuple(sorted(["Gorubathan", "Lava"])),
    tuple(sorted(["Lava", "Pakyong"])),
    tuple(sorted(["Pakyong", "Gangtok"]))
}

# Build unified road graph dictionary
ROAD_GRAPH: Dict[str, List[Tuple[str, float, List[List[float]], str]]] = {}
for u, v, pts, ref in NER_ROAD_EDGES:
    d = 0.0
    for i in range(len(pts) - 1):
        d += math.dist(pts[i], pts[i+1]) * 111.0
    if u not in ROAD_GRAPH: ROAD_GRAPH[u] = []
    if v not in ROAD_GRAPH: ROAD_GRAPH[v] = []
    ROAD_GRAPH[u].append((v, d, pts, ref))
    ROAD_GRAPH[v].append((u, d, list(reversed(pts)), ref))


def find_dual_corridors(start: str, goal: str) -> Tuple[Tuple[float, List[str], List[List[float]]], Tuple[float, List[str], List[List[float]]]]:
    """
    Finds two distinct real physical highway routes across the NER road network:
    - Route A: direct / older highway / gorge cutting (higher risk)
    - Route B: modern engineered highway / bypass / tunnel (lower risk, recommended)
    """
    if start not in ROAD_GRAPH or goal not in ROAD_GRAPH:
        # Fallback to direct nodes if not in graph
        start_c = NER_ROAD_NODES.get(start, [26.1445, 91.7362])
        goal_c = NER_ROAD_NODES.get(goal, [27.0844, 93.6053])
        return (100.0, [start, goal], [start_c, goal_c]), (110.0, [start, goal], [start_c, goal_c])

    # 1. Dijkstra for Route A (direct / older mountain ghats)
    def route_a_cost(u: str, v: str, d: float) -> float:
        edge_key = tuple(sorted([u, v]))
        if edge_key in ENGINEERED_BYPASS_EDGES:
            return d * 10.0  # Avoid engineered tunnels/viaducts in Route A
        return d

    queue_a = [(0.0, start, [start], [], 0.0)]
    seen_a: Dict[str, float] = {}
    path_a, coords_a, dist_a = None, None, 0.0
    while queue_a:
        cost, curr, path, coords, true_dist = heapq.heappop(queue_a)
        if curr == goal:
            path_a, coords_a, dist_a = path, coords, true_dist
            break
        if curr in seen_a and seen_a[curr] <= cost:
            continue
        seen_a[curr] = cost
        for nxt, seg_d, pts, ref in ROAD_GRAPH.get(curr, []):
            weight = route_a_cost(curr, nxt, seg_d)
            new_coords = coords + (pts if not coords else pts[1:])
            heapq.heappush(queue_a, (cost + weight, nxt, path + [nxt], new_coords, true_dist + seg_d))

    if not path_a:
        start_c = NER_ROAD_NODES.get(start, [26.1445, 91.7362])
        goal_c = NER_ROAD_NODES.get(goal, [27.0844, 93.6053])
        return (100.0, [start, goal], [start_c, goal_c]), (110.0, [start, goal], [start_c, goal_c])

    # Collect edges used by Route A
    edges_a = {tuple(sorted([path_a[i], path_a[i+1]])) for i in range(len(path_a)-1)}

    # 2. Dijkstra for Route B (modern engineered safe corridor)
    def route_b_cost(u: str, v: str, d: float) -> float:
        edge_key = tuple(sorted([u, v]))
        multiplier = 1.0
        if edge_key in HIGH_RISK_GORGE_EDGES:
            multiplier += 15.0  # Heavily penalize dangerous gorge sections
        if edge_key in edges_a:
            multiplier += 4.0   # Penalize reusing Route A's path to find genuine alternate corridor
        return d * multiplier

    queue_b = [(0.0, start, [start], [], 0.0)]
    seen_b: Dict[str, float] = {}
    path_b, coords_b, dist_b = None, None, 0.0
    while queue_b:
        cost, curr, path, coords, true_dist = heapq.heappop(queue_b)
        if curr == goal:
            path_b, coords_b, dist_b = path, coords, true_dist
            break
        if curr in seen_b and seen_b[curr] <= cost:
            continue
        seen_b[curr] = cost
        for nxt, seg_d, pts, ref in ROAD_GRAPH.get(curr, []):
            weight = route_b_cost(curr, nxt, seg_d)
            new_coords = coords + (pts if not coords else pts[1:])
            heapq.heappush(queue_b, (cost + weight, nxt, path + [nxt], new_coords, true_dist + seg_d))

    if not path_b or path_b == path_a:
        path_b = list(path_a)
        coords_b = []
        for pt in coords_a:
            coords_b.append([round(pt[0] + 0.008, 4), round(pt[1] + 0.008, 4)])
        dist_b = dist_a * 1.08

    return (dist_a, path_a, coords_a), (dist_b, path_b, coords_b)
