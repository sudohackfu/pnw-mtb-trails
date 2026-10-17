#!/usr/bin/env python3
"""
Exit 27 Unsanctioned Freeride Network Builder & Geospatial Audit Script

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   Endpoint: https://api.openstreetmap.org/api/0.6/map?bbox=-121.8750,47.4650,-121.8150,47.5050
2. King County Cadastral Parcel Database:
   Parcel PIN: 1423089001 (Rattlesnake Mountain NRCA, RCW 79.71)
3. WA DNR Public Forest Practices Transportation Layer:
   Forest road network & sanctioned Raging River trail corridors
4. Trailforks Raging River / Exit 27 Regional Records:
   Rider consensus names and difficulty ratings

Outputs Generated:
- exit27_unsanctioned_network.geojson
- exit27_unsanctioned_trails.kml
- exit27_unsanctioned_network.gpx
- exit27_active_freeride.gpx
- exit27_WILL_BE_decommissioned.gpx
- exit27_ALREADY_decommissioned.gpx
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Exit27-Builder/1.0'}
BBOX = (-121.8750, 47.4650, -121.8150, 47.5050)

# Explicit Sanctioned lines to exclude completely
SANCTIONED_EXCLUSIONS = {
    '1286010807', # Return Policy (main climbing trail)
    '1286010806', # Return Policy segment
    '1286010810', # Return Policy connector
    '1371077854', # Authorized connection
}

SANCTIONED_NAME_SUBSTRINGS = [
    'return policy', 'poppin', 'ccdh', 'canyon creek', 'invictus',
    'roaring ridge', 'physical therapy', 'raging tiger', 'no service',
    'snig', 'stanmar', 'pt', 'flow state', 'climb'
]

# Decommission targets
WILL_BE_DECOM_WAYS = {
    '1286010808': 'Return Policy Bypass North',
    '1286010809': 'Return Policy Bypass South',
    '1371077856': 'Deer',
    '1371077857': 'Cougar',
    '1371077858': 'Elk'
}

ALREADY_DECOM_WAYS = {
    '1286010811': 'Demolished Singletrack'
}

# Community names for formerly generic or unnamed lines (Option A Resolution)
OPTION_A_NAMES = {
    '1371077864': 'B-Line',
    '1371077852': 'Dingleberry',
    '1371077861': 'Smoke Break',
    '1371077862': 'Mainline Connector West',
    '1371077863': 'Mainline Connector East',
    '1371077860': 'Coal Train Link',
    '1371077859': 'Belly Dance Spur',
    '1371077865': 'B-Line North Link',
    '1371077866': 'B-Line South Link',
    '1371077867': 'Missionary Connector'
}

# Rating lookups
DOUBLE_BLACK_NAMES = {
    'Bruce Willis', 'Balls Deep', 'Oregon', 'Loam Star', 'Coal Train',
    'Supernatural', 'LSD', 'Lochsa', 'Belly Dance', 'Belly Dance Spur',
    'Demolished Singletrack'
}

def calculate_length_m(coords):
    total = 0.0
    for i in range(len(coords) - 1):
        lon1, lat1 = coords[i]
        lon2, lat2 = coords[i+1]
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        total += R * c
    return round(total, 2)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.dirname(script_dir)
    
    print("Fetching Exit 27 OSM vector data...")
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}"
    r = requests.get(url, headers=HEADERS, timeout=60)
    if r.status_code != 200:
        print(f"Error fetching data: HTTP {r.status_code}")
        sys.exit(1)
        
    root = ET.fromstring(r.content)
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
        
    features = []
    
    for way in root.findall('way'):
        wid = way.attrib['id']
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
        hw = tags.get('highway')
        if hw not in ['path', 'footway', 'cycleway', 'track']:
            continue
            
        raw_name = tags.get('name', '').strip()
        
        # Check sanctioned exclusions
        if wid in SANCTIONED_EXCLUSIONS:
            continue
        if any(sub in raw_name.lower() for sub in SANCTIONED_NAME_SUBSTRINGS):
            continue
            
        # Isolate coordinates
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        if len(coords) < 2:
            continue
            
        # Naming resolution
        if wid in WILL_BE_DECOM_WAYS:
            name = WILL_BE_DECOM_WAYS[wid]
            status = "WILL BE Decommissioned"
            hex_color = "#ea580c"
            difficulty = "Black Diamond"
            imba_val = 3
        elif wid in ALREADY_DECOM_WAYS:
            name = ALREADY_DECOM_WAYS[wid]
            status = "ALREADY Decommissioned"
            hex_color = "#475569"
            difficulty = "Double Black Diamond"
            imba_val = 4
        else:
            if wid in OPTION_A_NAMES:
                name = OPTION_A_NAMES[wid]
            elif raw_name:
                name = raw_name
            else:
                name = f"Freeride Spur ({wid})"
                
            status = "Active Freeride"
            if name in DOUBLE_BLACK_NAMES or 'double' in name.lower():
                difficulty = "Double Black Diamond"
                hex_color = "#000000"
                imba_val = 4
            else:
                difficulty = "Black Diamond"
                hex_color = "#dc2626"
                imba_val = 3
                
        length_m = calculate_length_m(coords)
        
        feature = {
            'type': 'Feature',
            'id': wid,
            'properties': {
                'name': name,
                'status': status,
                'difficulty': difficulty,
                'imba_scale': imba_val,
                'stroke': hex_color,
                'stroke-width': 4.0,
                'length_m': length_m,
                'osm_id': wid,
                'tags': tags
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        }
        features.append(feature)
        
    print(f"Processed {len(features)} unsanctioned Exit 27 trails.")
    
    # 1. Export Master GeoJSON
    with open(os.path.join(target_dir, "exit27_unsanctioned_network.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f, indent=2)
        
    # 2. Export KML 2.2
    export_kml(features, os.path.join(target_dir, "exit27_unsanctioned_trails.kml"))
    
    # 3. Export Master GPX
    export_gpx(features, os.path.join(target_dir, "exit27_unsanctioned_network.gpx"), "Exit 27 Unsanctioned Master")
    
    # 4. Export Separated GPX Layers
    will_decom = [f for f in features if f['properties']['status'] == "WILL BE Decommissioned"]
    already_decom = [f for f in features if f['properties']['status'] == "ALREADY Decommissioned"]
    active = [f for f in features if f['properties']['status'] == "Active Freeride"]
    
    export_gpx(will_decom, os.path.join(target_dir, "exit27_WILL_BE_decommissioned.gpx"), "Exit 27 - WILL BE Decommissioned")
    export_gpx(already_decom, os.path.join(target_dir, "exit27_ALREADY_decommissioned.gpx"), "Exit 27 - ALREADY Decommissioned")
    export_gpx(active, os.path.join(target_dir, "exit27_active_freeride.gpx"), "Exit 27 - Active Freeride")
    print("All Exit 27 vector layers successfully generated.")

def export_kml(features, filepath):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
    lines.append('  <Document>')
    lines.append('    <name>Exit 27 Unsanctioned Trails</name>')
    
    colors = set(f['properties']['stroke'] for f in features)
    for c in colors:
        clean = c.replace('#', '')
        kml_col = 'ff' + clean[4:6] + clean[2:4] + clean[0:2]
        lines.append(f'    <Style id="style_{clean}">')
        lines.append('      <LineStyle>')
        lines.append(f'        <color>{kml_col}</color>')
        lines.append('        <width>4</width>')
        lines.append('      </LineStyle>')
        lines.append('    </Style>')
        
    for f in features:
        props = f['properties']
        clean = props['stroke'].replace('#', '')
        coords_str = ' '.join(f"{lon},{lat},0" for lon, lat in f['geometry']['coordinates'])
        lines.append('    <Placemark>')
        lines.append(f"      <name><![CDATA[{props['name']}]]></name>")
        lines.append(f"      <description><![CDATA[Difficulty: {props['difficulty']}<br>Status: {props['status']}<br>Length: {props['length_m']} m]]></description>")
        lines.append(f"      <styleUrl>#style_{clean}</styleUrl>")
        lines.append('      <LineString>')
        lines.append('        <tessellate>1</tessellate>')
        lines.append(f"        <coordinates>{coords_str}</coordinates>")
        lines.append('      </LineString>')
        lines.append('    </Placemark>')
    lines.append('  </Document>')
    lines.append('</kml>')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))

def export_gpx(features, filepath, layer_name):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<gpx version="1.1" creator="Exit27Builder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">')
    lines.append(f'  <metadata><name>{layer_name}</name></metadata>')
    for f in features:
        props = f['properties']
        lines.append('  <trk>')
        lines.append(f"    <name><![CDATA[{props['name']}]]></name>")
        lines.append(f"    <desc><![CDATA[Status: {props['status']} | Difficulty: {props['difficulty']}]]></desc>")
        lines.append('    <extensions>')
        lines.append(f"      <tf:difficulty>{props['imba_scale']}</tf:difficulty>")
        lines.append(f"      <tf:color>{props['stroke']}</tf:color>")
        lines.append('      <gpxx:TrackExtension>')
        lines.append(f"        <gpxx:DisplayColor>{props['stroke']}</gpxx:DisplayColor>")
        lines.append('      </gpxx:TrackExtension>')
        lines.append('    </extensions>')
        lines.append('    <trkseg>')
        for lon, lat in f['geometry']['coordinates']:
            lines.append(f'      <trkpt lat="{lat}" lon="{lon}"/>')
        lines.append('    </trkseg>')
        lines.append('  </trk>')
    lines.append('</gpx>')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
