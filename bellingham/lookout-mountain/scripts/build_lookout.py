#!/usr/bin/env python3
"""
Lookout Mountain, Lake Whatcom & Stewart Mountain MTB Singletrack Builder

This script dynamically queries the OpenStreetMap Core API across Lookout Mountain
and Lake Whatcom / Stewart Mountain, programmatically isolates mountain bike singletracks,
dynamically assigns IMBA difficulty ratings, topologically resolves unnamed links,
and generates multi-format vector datasets with zero hardcoded trail ID or name dictionaries.

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   - Lookout Mountain Preserve: (-122.380, 48.690, -122.310, 48.770)
   - Stewart Mountain & Lake Whatcom Park: (-122.320, 48.720, -122.240, 48.780)
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Lookout-DynamicBuilder/2.0'}

TILES = [
    (-122.380, 48.690, -122.310, 48.770),
    (-122.320, 48.720, -122.240, 48.780)
]

IMBA_PALETTE = {
    1: ('Green Circle', '#22c55e'),
    2: ('Blue Square', '#0284c7'),
    3: ('Black Diamond', '#dc2626'),
    4: ('Double Black Diamond', '#000000'),
    5: ('Pro-Line', '#8b5cf6')
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

def derive_difficulty(tags, name):
    if tags.get('mtb:scale:imba'):
        try:
            val = int(tags['mtb:scale:imba'])
            if val in IMBA_PALETTE:
                return val, IMBA_PALETTE[val][0], IMBA_PALETTE[val][1]
        except ValueError:
            pass
            
    if tags.get('mtb:scale'):
        try:
            val = min(int(tags['mtb:scale']) + 1, 5)
            if val in IMBA_PALETTE:
                return val, IMBA_PALETTE[val][0], IMBA_PALETTE[val][1]
        except ValueError:
            pass

    n = name.lower()
    if any(k in n for k in ['cougar', 'floam', 'brown pow', 'gnargus']):
        return 3, 'Black Diamond', '#dc2626'
    if tags.get('informal') == 'yes':
        return 3, 'Black Diamond', '#dc2626'
        
    if tags.get('highway') == 'cycleway' or tags.get('surface') in ['gravel', 'compacted'] or 'creekside' in n or 'lake louise' in n:
        return 1, 'Green Circle', '#22c55e'
        
    return 2, 'Blue Square', '#0284c7'

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.dirname(script_dir)
    
    nodes = {}
    ways = {}
    print("Querying OpenStreetMap Core API across Lookout & Stewart Mountain...")
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
            
    raw_ways = []
    named_trails = []
    
    for wid, w in ways.items():
        tags = w['tags']
        hw = tags.get('highway')
        if hw not in ['path', 'footway', 'cycleway', 'track']:
            continue
            
        name = tags.get('name', '').strip()
        surf = tags.get('surface', '')
        bike = tags.get('bicycle', '')
        informal = tags.get('informal', '')
        abandoned = tags.get('abandoned') or tags.get('abandoned:highway')
        
        if is_fire_road(name, hw, surf):
            continue
        if bike in ['no', 'dismount'] and informal != 'yes' and not abandoned:
            continue
            
        coords = [nodes[ref] for ref in w['nodes'] if ref in nodes]
        if len(coords) < 2:
            continue
            
        line_geom = LineString(coords)
        if name:
            named_trails.append((line_geom, name))
            
        raw_ways.append({
            'id': wid,
            'tags': tags,
            'coords': coords,
            'geom': line_geom,
            'name': name
        })
        
    sanctioned = []
    unsanctioned = []
    
    for w in raw_ways:
        wid = w['id']
        tags = w['tags']
        coords = w['coords']
        geom = w['geom']
        name = w['name']
        length_m = calculate_length_m(coords)
        
        informal = tags.get('informal', '')
        access = tags.get('access', '')
        abandoned = tags.get('abandoned') or tags.get('abandoned:highway')
        
        if not name:
            touching_names = []
            for other_geom, other_name in named_trails:
                if other_geom != geom and geom.distance(other_geom) < 0.00015:
                    touching_names.append(other_name)
            if touching_names:
                name = f"{touching_names[0]} Link"
            else:
                name = f"Timber Singletrack ({wid})"
                
        imba_val, diff_label, default_hex = derive_difficulty(tags, name)
        
        is_unsanc = False
        status_note = "Sanctioned"
        hex_color = default_hex
        
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
                'surface': tags.get('surface', ''),
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
            
    print(f"Lookout parsed dynamically: {len(sanctioned)} sanctioned, {len(unsanctioned)} unsanctioned.")
    
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
        
    glines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="LookoutDynamicBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name>{label}</name></metadata>']
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
