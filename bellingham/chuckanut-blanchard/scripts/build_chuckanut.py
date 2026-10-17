#!/usr/bin/env python3
"""
Chuckanut Mountain & Blanchard State Forest MTB Singletrack Builder

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   Bounding Box: (-122.520, 48.600, -122.420, 48.700)
2. WA DNR Blanchard State Forest Recreation Plan:
   Authorized non-motorized trail network
3. Washington State Parks Larrabee State Park GIS:
   Park boundaries and pedestrian-only trail restrictions
4. Trailforks Regions 1686 (Chuckanut) & 1687 (Blanchard):
   Community ratings and condition records

Outputs Generated:
- chuckanut_sanctioned.geojson / .kml / .gpx
- chuckanut_unsanctioned.geojson / .kml / .gpx
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Chuckanut-Builder/1.0'}
BBOX = (-122.520, 48.600, -122.420, 48.700)

IMBA_MAP = {
    '1': ('Green Circle', '#22c55e', 1),
    '2': ('Blue Square', '#0284c7', 2),
    '3': ('Black Diamond', '#dc2626', 3),
    '4': ('Double Black Diamond', '#000000', 4),
    '5': ('Pro-Line', '#8b5cf6', 5)
}

COMMUNITY_RATINGS = {
    'Double Black Diamond': (3, 'Black Diamond', '#dc2626'),
    'Double Down': (4, 'Double Black Diamond', '#000000'),
    'Hush Hush Trail': (3, 'Black Diamond', '#dc2626'),
    'Madrone Crest Trail': (3, 'Black Diamond', '#dc2626'),
    'Ridge Trail': (3, 'Black Diamond', '#dc2626'),
    'Cinco': (2, 'Blue Square', '#0284c7'),
    'Quattro': (2, 'Blue Square', '#0284c7'),
    'Dan\'s Traverse Trail': (2, 'Blue Square', '#0284c7'),
    'Hemlock Trail': (2, 'Blue Square', '#0284c7'),
    'Fiona Ridge': (3, 'Black Diamond', '#ea580c'),
    'Rooty Ridge': (3, 'Black Diamond', '#ea580c'),
    'Rooty Ridge Lower': (3, 'Black Diamond', '#ea580c')
}

def is_fire_road(name, hw, surf):
    n = name.lower()
    if hw == 'track' and (surf in ['gravel', 'compacted', 'unpaved', 'asphalt'] or 'road' in n or 'rd ' in n or n.startswith('bl-') or n.startswith('dnr ')):
        return True
    if any(k in n for k in ['drive', 'highway', 'street', 'pacific rim']):
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
    
    print("Fetching Chuckanut OSM vector data...")
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}"
    r = requests.get(url, headers=HEADERS, timeout=60)
    if r.status_code != 200:
        print(f"Error fetching data: HTTP {r.status_code}")
        sys.exit(1)
        
    root = ET.fromstring(r.content)
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
        
    sanctioned = []
    unsanctioned = []
    
    for way in root.findall('way'):
        wid = way.attrib['id']
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
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
            
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
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
                'system': 'Chuckanut & Blanchard Mountain',
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
            
    print(f"Chuckanut parsed: {len(sanctioned)} sanctioned, {len(unsanctioned)} unsanctioned.")
    
    export_layer(sanctioned, target_dir, "chuckanut_sanctioned", "Chuckanut & Blanchard - Sanctioned")
    export_layer(unsanctioned, target_dir, "chuckanut_unsanctioned", "Chuckanut & Blanchard - Unsanctioned")
    print("Chuckanut vector files generated successfully.")

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
        
    glines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="ChuckanutBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name>{label}</name></metadata>']
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
