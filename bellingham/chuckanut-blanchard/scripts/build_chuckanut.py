#!/usr/bin/env python3
"""
Chuckanut Mountain & Blanchard State Forest MTB Singletrack Builder

This script implements the Programmatic-First with Community-Index Override architecture:
1. Queries the OpenStreetMap Core API across Chuckanut & Blanchard.
2. Applies strict physical singletrack isolation: excludes logging roads / fire roads
   (e.g., Cleator Road, Fragrance Lake Road, BL-1616) and pedestrian-only paths.
3. Resolves names via the canonical hierarchy:
   a. Community Index Override: if way ID has "override": true in community_index.json,
      applies vetted community name, difficulty, and status.
   b. Programmatic API Name: uses OSM name if present and authentic.
   c. Topological Spatial Resolution: connects unnamed spurs to parent trails as "{Parent} Link".
   d. Unresearched Generic Exclusion: unverified lines without an override or authentic name
      are excluded from export so zero generic IDs reach the vector files.
4. Generates sanitized GeoJSON, KML 2.2, and GPX 1.1 datasets for both Sanctioned
   and Unsanctioned networks with zero prefix clutter.

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   Bounding Box: (-122.520, 48.600, -122.420, 48.700)
2. Community Trail Index:
   File: community_index.json (Vetted rider names, ratings, and status metadata)
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Chuckanut-DynamicBuilder/3.0'}
BBOX = (-122.520, 48.600, -122.420, 48.700)

IMBA_PALETTE = {
    1: ('Green Circle', '#22c55e'),
    2: ('Blue Square', '#0284c7'),
    3: ('Black Diamond', '#dc2626'),
    4: ('Double Black Diamond', '#000000'),
    5: ('Pro-Line', '#8b5cf6')
}

def is_fire_road(name, hw, surf):
    n = name.lower()
    if 'road' in n or ' rd' in n or n.startswith('rd ') or n.endswith(' rd') or n.startswith('bl-') or n.startswith('dnr '):
        return True
    if hw == 'track' and (surf in ['gravel', 'compacted', 'unpaved', 'asphalt'] or not surf):
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
    if 'double down' in n or 'horn' in n:
        return 4, 'Double Black Diamond', '#000000'
    if any(k in n for k in ['black diamond', 'hush', 'fiona', 'rooty', 'ridge', 'madrone', 'chute']):
        return 3, 'Black Diamond', '#dc2626'
    if tags.get('informal') == 'yes':
        return 3, 'Black Diamond', '#dc2626'
        
    if tags.get('highway') == 'cycleway' or tags.get('surface') in ['gravel', 'compacted'] or 'interurban' in n or 'clayton' in n:
        return 1, 'Green Circle', '#22c55e'
        
    return 2, 'Blue Square', '#0284c7'

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.dirname(script_dir)
    index_path = os.path.join(script_dir, "community_index.json")
    
    # 1. Load Community Trail Index
    community_index = {}
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            community_index = json.load(f)
        print(f"Loaded {len(community_index)} records from Chuckanut community_index.json")
    
    # 2. Query OSM Core API
    print("Querying OpenStreetMap Core API for Chuckanut & Blanchard...")
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}"
    r = requests.get(url, headers=HEADERS, timeout=60)
    if r.status_code != 200:
        print(f"Failed to fetch OSM data: HTTP {r.status_code}")
        sys.exit(1)
        
    root = ET.fromstring(r.content)
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
        
    raw_ways = []
    named_trails = []
    
    for way in root.findall('way'):
        wid = way.attrib['id']
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
        hw = tags.get('highway')
        if hw not in ['path', 'footway', 'cycleway', 'track']:
            continue
            
        name = tags.get('name', '').strip()
        surf = tags.get('surface', '')
        bike = tags.get('bicycle', '')
        informal = tags.get('informal', '')
        abandoned = tags.get('abandoned') or tags.get('abandoned:highway')
        
        # Physical singletrack filtering: exclude fire roads
        if is_fire_road(name, hw, surf):
            continue
            
        # Pedestrian exclusion: exclude bicycle-forbidden paths
        if bike in ['no', 'dismount'] and informal != 'yes' and not abandoned:
            continue
            
        # Exclude pedestrian footways without bicycle access unless community override exists
        if hw == 'footway' and bike not in ['yes', 'designated'] and wid not in community_index:
            continue
            
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
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
    excluded_count = 0
    
    for w in raw_ways:
        wid = w['id']
        tags = w['tags']
        coords = w['coords']
        geom = w['geom']
        name = w['name']
        length_m = calculate_length_m(coords)
        
        # Check Community Index Override first
        if wid in community_index and community_index[wid].get('override'):
            c_info = community_index[wid]
            name = c_info['name']
            diff_label = c_info.get('difficulty', 'Black Diamond')
            status_note = c_info.get('status', 'Unsanctioned (Community Built)')
            hex_color = c_info.get('stroke', '#ea580c')
            imba_val = c_info.get('imba_scale', 3)
            is_unsanc = True
        else:
            # Fall back to programmatic name
            if not name:
                touching_names = []
                for other_geom, other_name in named_trails:
                    if other_geom != geom and geom.distance(other_geom) < 0.00015:
                        touching_names.append(other_name)
                if touching_names:
                    name = f"{touching_names[0]} Link"
                else:
                    # Unverified generic spur without override -> Exclude from export
                    excluded_count += 1
                    continue
                    
            imba_val, diff_label, default_hex = derive_difficulty(tags, name)
            informal = tags.get('informal', '')
            access = tags.get('access', '')
            abandoned = tags.get('abandoned') or tags.get('abandoned:highway')
            
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
                'system': 'Chuckanut & Blanchard Mountain',
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
            
    print(f"Chuckanut processed: {len(sanctioned)} sanctioned, {len(unsanctioned)} unsanctioned, {excluded_count} unverified spurs excluded.")
    
    export_layer(sanctioned, target_dir, "chuckanut_sanctioned", "Chuckanut and Blanchard - Sanctioned")
    export_layer(unsanctioned, target_dir, "chuckanut_unsanctioned", "Chuckanut and Blanchard - Unsanctioned")
    print("Chuckanut vector files generated successfully.")

def export_layer(features, out_dir, prefix, label):
    with open(os.path.join(out_dir, f"{prefix}.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f, indent=2)
        
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2">', '  <Document>', f'    <name><![CDATA[{label}]]></name>']
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
        
    glines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="ChuckanutDynamicBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name><![CDATA[{label}]]></name></metadata>']
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
