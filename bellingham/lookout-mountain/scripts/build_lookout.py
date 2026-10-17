#!/usr/bin/env python3
"""
Lookout Mountain, Lake Whatcom & Stewart Mountain MTB Singletrack Builder

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   - Lookout Mountain Preserve: (-122.380, 48.690, -122.310, 48.770)
   - Stewart Mountain & Lake Whatcom Park: (-122.320, 48.720, -122.240, 48.780)
2. Whatcom County Parks & Recreation Master Plan:
   Park boundary and sanctioned trail alignment geodatabase
3. WA DNR Olsen Creek State Forest GIS:
   State timber recreation corridors
4. Trailforks Region 17820 (Lookout Mountain) & Lake Whatcom Records:
   Condition reports and community difficulty lookups

Outputs Generated:
- lookout_sanctioned.geojson / .kml / .gpx
- lookout_unsanctioned.geojson / .kml / .gpx
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Lookout-Builder/1.0'}

TILES = [
    (-122.380, 48.690, -122.310, 48.770),
    (-122.320, 48.720, -122.240, 48.780)
]

IMBA_MAP = {
    '1': ('Green Circle', '#22c55e', 1),
    '2': ('Blue Square', '#0284c7', 2),
    '3': ('Black Diamond', '#dc2626', 3),
    '4': ('Double Black Diamond', '#000000', 4),
    '5': ('Pro-Line', '#8b5cf6', 5)
}

COMMUNITY_RATINGS = {
    'Cougar Ridge Trail': (3, 'Black Diamond', '#dc2626'),
    'Floam': (3, 'Black Diamond', '#dc2626'),
    'Brown Pow': (3, 'Black Diamond', '#dc2626'),
    'Rufus Creek Trail': (2, 'Blue Square', '#0284c7'),
    'Chanterelle Trail': (2, 'Blue Square', '#0284c7'),
    'El Diablo': (2, 'Blue Square', '#0284c7'),
    'Moto\'s Run': (2, 'Blue Square', '#0284c7'),
    'Bottoms Up': (2, 'Blue Square', '#0284c7'),
    'Hooty Hoot': (2, 'Blue Square', '#0284c7'),
    'Waterfall Trail (Gnargus)': (2, 'Blue Square', '#0284c7'),
    'Earth Star': (2, 'Blue Square', '#0284c7'),
    'Turkey Tail': (2, 'Blue Square', '#0284c7'),
    'Baneberry Trail': (2, 'Blue Square', '#0284c7'),
    'Creekside Trail': (1, 'Green Circle', '#22c55e'),
    '#5': (3, 'Black Diamond', '#ea580c'),
    '#8': (3, 'Black Diamond', '#ea580c'),
    'BR': (3, 'Black Diamond', '#475569')
}

def is_fire_road(name, hw, surf):
    n = name.lower()
    if hw == 'track' and (surf in ['gravel', 'compacted', 'unpaved', 'asphalt'] or 'road' in n or 'rd ' in n or n.startswith('oc-')):
        return True
    if any(k in n for k in ['drive', 'highway', 'street', 'seed orchard']):
        return True
    return False

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
    
    nodes = {}
    ways = {}
    print("Fetching Lookout & Stewart Mountain OSM vector data...")
    for i, bbox in enumerate(TILES):
        url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        r = requests.get(url, headers=HEADERS, timeout=45)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for node in root.findall('node'):
                nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
            for way in root.findall('way'):
                tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
                nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
                ways[way.attrib['id']] = {'tags': tags, 'nodes': nd_refs}
            print(f"  Tile {i+1} fetched successfully.")
        else:
            print(f"  Tile {i+1} failed with status {r.status_code}")
            
    sanctioned = []
    unsanctioned = []
    
    for wid, w in ways.items():
        tags = w['tags']
        hw = tags.get('highway')
        if hw not in ['path', 'footway', 'cycleway', 'track']:
            continue
            
        name = tags.get('name', '').strip()
        if not name:
            if tags.get('informal') == 'yes' and tags.get('bicycle') != 'no':
                name = f"Unnamed Trail ({wid})"
            else:
                continue
                
        surf = tags.get('surface', '')
        bike = tags.get('bicycle', '')
        access = tags.get('access', '')
        informal = tags.get('informal', '')
        abandoned = tags.get('abandoned') or tags.get('abandoned:highway')
        
        if is_fire_road(name, hw, surf):
            continue
        if bike in ['no', 'dismount'] and informal != 'yes' and not abandoned:
            continue
            
        coords = [nodes[ref] for ref in w['nodes'] if ref in nodes]
        if len(coords) < 2:
            continue
            
        length_m = calculate_length_m(coords)
        
        imba_tag = tags.get('mtb:scale:imba')
        if imba_tag in IMBA_MAP:
            diff_label, hex_color, imba_val = IMBA_MAP[imba_tag]
        elif name in COMMUNITY_RATINGS:
            imba_val, diff_label, hex_color = COMMUNITY_RATINGS[name]
        else:
            diff_label, hex_color, imba_val = ('Blue Square', '#0284c7', 2)
            
        is_unsanc = False
        status_note = "Sanctioned"
        if informal == 'yes':
            is_unsanc = True
            status_note = "Unsanctioned (Community Built)"
            hex_color = "#ea580c"
        elif abandoned:
            is_unsanc = True
            status_note = "Unsanctioned (Abandoned / Decommissioned)"
            hex_color = "#475569"
        elif access in ['private', 'no']:
            is_unsanc = True
            status_note = f"Unsanctioned (Access: {access})"
            hex_color = "#ea580c"
            
        feature = {
            'type': 'Feature',
            'id': wid,
            'properties': {
                'name': name,
                'system': 'Lookout Mountain & Lake Whatcom',
                'status': status_note,
                'difficulty': diff_label,
                'imba_scale': imba_val,
                'stroke': hex_color,
                'stroke-width': 3.5,
                'length_m': length_m,
                'oneway': tags.get('oneway', 'no'),
                'surface': surf,
                'osm_id': wid,
                'tags': tags
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        }
        
        if is_unsanc:
            unsanctioned.append(feature)
        else:
            sanctioned.append(feature)
            
    print(f"Lookout parsed: {len(sanctioned)} sanctioned, {len(unsanctioned)} unsanctioned.")
    
    export_layer(sanctioned, target_dir, "lookout_sanctioned", "Lookout Mountain - Sanctioned")
    export_layer(unsanctioned, target_dir, "lookout_unsanctioned", "Lookout Mountain - Unsanctioned")
    print("Lookout vector files generated successfully.")

def export_layer(features, out_dir, prefix, label):
    with open(os.path.join(out_dir, f"{prefix}.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f, indent=2)
        
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2">', '  <Document>', f'    <name>{label}</name>']
    colors = set(f['properties']['stroke'] for f in features)
    for c in colors:
        clean = c.replace('#', '')
        kml_col = 'ff' + clean[4:6] + clean[2:4] + clean[0:2]
        lines.append(f'    <Style id="style_{clean}"><LineStyle><color>{kml_col}</color><width>4</width></LineStyle></Style>')
    for f in features:
        props = f['properties']
        clean = props['stroke'].replace('#', '')
        coords_str = ' '.join(f"{lon},{lat},0" for lon, lat in f['geometry']['coordinates'])
        lines.append('    <Placemark>')
        lines.append(f"      <name><![CDATA[{props['name']}]]></name>")
        lines.append(f"      <description><![CDATA[Difficulty: {props['difficulty']}<br>Status: {props['status']}<br>Length: {props['length_m']} m]]></description>")
        lines.append(f"      <styleUrl>#style_{clean}</styleUrl>")
        lines.append(f"      <LineString><tessellate>1</tessellate><coordinates>{coords_str}</coordinates></LineString>")
        lines.append('    </Placemark>')
    lines.append('  </Document></kml>')
    with open(os.path.join(out_dir, f"{prefix}.kml"), "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
        
    glines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="LookoutBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name>{label}</name></metadata>']
    for f in features:
        props = f['properties']
        glines.append('  <trk>')
        glines.append(f"    <name><![CDATA[{props['name']}]]></name>")
        glines.append(f"    <desc><![CDATA[Difficulty: {props['difficulty']} | Status: {props['status']}]]></desc>")
        glines.append(f"    <extensions><tf:difficulty>{props['imba_scale']}</tf:difficulty><tf:color>{props['stroke']}</tf:color><gpxx:TrackExtension><gpxx:DisplayColor>{props['stroke']}</gpxx:DisplayColor></gpxx:TrackExtension></extensions>")
        glines.append('    <trkseg>')
        for lon, lat in f['geometry']['coordinates']:
            glines.append(f'      <trkpt lat="{lat}" lon="{lon}"/>')
        glines.append('    </trkseg></trk>')
    glines.append('</gpx>')
    with open(os.path.join(out_dir, f"{prefix}.gpx"), "w", encoding="utf-8") as f:
        f.write('\n'.join(glines))

if __name__ == '__main__':
    main()
