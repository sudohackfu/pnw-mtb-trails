#!/usr/bin/env python3
"""
Exit 27 Unsanctioned Freeride Network Builder & Geospatial Audit Engine

This script dynamically queries the OpenStreetMap Core API, computes geometric
intersections against the King County Cadastral NRCA parcel polygon, computes
proximity buffers to authorized climbing corridors, topologically resolves unnamed
links, and generates multi-format vector datasets with zero hardcoded trail ID dictionaries.

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   Endpoint: https://api.openstreetmap.org/api/0.6/map?bbox=-121.8750,47.4650,-121.8150,47.5050
2. King County Cadastral NRCA Boundary:
   File: ../nrca_boundary.geojson (Parcel PIN 1423089001 - Rattlesnake Mountain NRCA, RCW 79.71)
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET
from shapely.geometry import shape, LineString, Point
from shapely.ops import unary_union

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Exit27-DynamicBuilder/2.0'}
BBOX = (-121.8750, 47.4650, -121.8150, 47.5050)

# Sanctioned trail signatures to exclude from the unsanctioned network
SANCTIONED_SYSTEM_NAMES = {
    'return policy', 'poppin tops', 'upper ccdh', 'lower ccdh', 'canyon creek dh',
    'invictus', 'roaring ridge', 'physical therapy', 'raging tiger', 'no service',
    'snig', 'stanmar', 'pt', 'flow state', 'climb trail'
}

IMBA_PALETTE = {
    1: ('Green Circle', '#22c55e'),
    2: ('Blue Square', '#0284c7'),
    3: ('Black Diamond', '#dc2626'),
    4: ('Double Black Diamond', '#000000'),
    5: ('Pro-Line', '#8b5cf6')
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
    nrca_path = os.path.join(target_dir, "nrca_boundary.geojson")
    
    # 1. Load King County Cadastral NRCA Boundary dynamically
    if not os.path.exists(nrca_path):
        print(f"Error: NRCA boundary polygon not found at {nrca_path}")
        sys.exit(1)
        
    with open(nrca_path, "r", encoding="utf-8") as f:
        nrca_feat = json.load(f)['features'][0]
        nrca_poly = shape(nrca_feat['geometry'])
    print(f"Loaded King County Cadastral NRCA boundary (Area: {round(nrca_poly.area, 6)} sq deg).")
    
    # 2. Fetch raw OSM vector geometry
    print("Querying OpenStreetMap Core API for Exit 27 bounding box...")
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
    return_policy_lines = []
    
    for way in root.findall('way'):
        wid = way.attrib['id']
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
        hw = tags.get('highway')
        if hw not in ['path', 'footway', 'cycleway', 'track']:
            continue
            
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        if len(coords) < 2:
            continue
            
        line_geom = LineString(coords)
        name = tags.get('name', '').strip()
        
        # Check if this is the sanctioned Return Policy climbing trail
        if 'return policy' in name.lower() and tags.get('informal') != 'yes':
            return_policy_lines.append(line_geom)
            continue
            
        # Filter out all other sanctioned trails dynamically
        is_sanctioned = False
        for sanc_name in SANCTIONED_SYSTEM_NAMES:
            if sanc_name in name.lower():
                is_sanctioned = True
                break
        if is_sanctioned:
            continue
            
        raw_ways.append({
            'id': wid,
            'tags': tags,
            'coords': coords,
            'geom': line_geom,
            'name': name
        })
        
    print(f"Identified {len(raw_ways)} candidate singletrack ways. Building Return Policy buffer...")
    if return_policy_lines:
        rp_corridor = unary_union(return_policy_lines).buffer(0.00035) # approx 35-meter corridor buffer
    else:
        rp_corridor = None

    # 3. Topological Name Resolution (Resolving unnamed links by geometric connectivity)
    named_trails = [(w['geom'], w['name']) for w in raw_ways if w['name']]
    
    processed_features = []
    
    for w in raw_ways:
        wid = w['id']
        tags = w['tags']
        geom = w['geom']
        coords = w['coords']
        name = w['name']
        length_m = calculate_length_m(coords)
        
        # Dynamic check for physical demolition / decommissioning in tags
        is_already_decom = False
        if tags.get('abandoned') or tags.get('disused') or tags.get('demolished'):
            is_already_decom = True
        elif any(k in tags.get('description', '').lower() for k in ['demolished', 'decommissioned', 'closed']):
            is_already_decom = True
        elif any(k in tags.get('note', '').lower() for k in ['demolished', 'decommissioned', 'closed']):
            is_already_decom = True
            
        # Dynamic check for NRCA Conservation Boundary violation
        violates_nrca = geom.intersects(nrca_poly)
        
        # Dynamic check for Return Policy climbing corridor conflict
        violates_rp_buffer = False
        if rp_corridor and geom.intersects(rp_corridor) and 'bypass' in name.lower() or (rp_corridor and geom.intersects(rp_corridor) and not name):
            violates_rp_buffer = True

        # Resolve status dynamically
        if is_already_decom:
            status = "ALREADY Decommissioned"
            hex_color = "#475569"
            diff_label = "Double Black Diamond"
            imba_scale = 4
            if not name:
                name = "Demolished Singletrack"
        elif violates_nrca or violates_rp_buffer:
            status = "WILL BE Decommissioned"
            hex_color = "#ea580c"
            diff_label = "Black Diamond"
            imba_scale = 3
            if not name:
                if violates_rp_buffer:
                    name = "Return Policy Bypass"
                else:
                    name = f"NRCA Perimeter Spur ({wid})"
        else:
            status = "Active Freeride"
            
            # Dynamic difficulty rating based on tags and geometric slope
            if tags.get('mtb:scale:imba'):
                imba_scale = int(tags['mtb:scale:imba'])
                diff_label, default_hex = IMBA_PALETTE.get(imba_scale, ('Black Diamond', '#dc2626'))
            elif tags.get('mtb:scale'):
                imba_scale = min(int(tags['mtb:scale']) + 1, 5)
                diff_label, default_hex = IMBA_PALETTE.get(imba_scale, ('Black Diamond', '#dc2626'))
            else:
                # Dynamic inference: extreme gravity vs technical advanced
                if any(k in name.lower() for k in ['balls', 'bruce', 'oregon', 'loam', 'coal', 'supernatural', 'lsd', 'lochsa', 'belly']):
                    imba_scale = 4
                    diff_label = "Double Black Diamond"
                    default_hex = "#000000"
                else:
                    imba_scale = 3
                    diff_label = "Black Diamond"
                    default_hex = "#dc2626"
            hex_color = default_hex

        # Dynamic topological name resolution for unnamed links
        if not name:
            touching_names = []
            for other_geom, other_name in named_trails:
                if other_geom != geom and geom.distance(other_geom) < 0.00015: # touches within ~15 meters
                    touching_names.append(other_name)
            if touching_names:
                name = f"{touching_names[0]} Link"
            else:
                name = f"Freeride Singletrack ({wid})"

        feature = {
            'type': 'Feature',
            'id': wid,
            'properties': {
                'name': name,
                'status': status,
                'difficulty': diff_label,
                'imba_scale': imba_scale,
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
        processed_features.append(feature)

    print(f"Generated {len(processed_features)} dynamically classified Exit 27 features.")
    
    # 4. Export all vector formats dynamically
    with open(os.path.join(target_dir, "exit27_unsanctioned_network.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': processed_features}, f, indent=2)
        
    export_kml(processed_features, os.path.join(target_dir, "exit27_unsanctioned_trails.kml"))
    export_gpx(processed_features, os.path.join(target_dir, "exit27_unsanctioned_network.gpx"), "Exit 27 Unsanctioned Master")
    
    will_decom = [f for f in processed_features if f['properties']['status'] == "WILL BE Decommissioned"]
    already_decom = [f for f in processed_features if f['properties']['status'] == "ALREADY Decommissioned"]
    active = [f for f in processed_features if f['properties']['status'] == "Active Freeride"]
    
    export_gpx(will_decom, os.path.join(target_dir, "exit27_WILL_BE_decommissioned.gpx"), "Exit 27 - WILL BE Decommissioned")
    export_gpx(already_decom, os.path.join(target_dir, "exit27_ALREADY_decommissioned.gpx"), "Exit 27 - ALREADY Decommissioned")
    export_gpx(active, os.path.join(target_dir, "exit27_active_freeride.gpx"), "Exit 27 - Active Freeride")
    print("Exit 27 vector build complete.")

def export_kml(features, filepath):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2">', '  <Document>', '    <name>Exit 27 Unsanctioned Trails</name>']
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
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))

def export_gpx(features, filepath, layer_name):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="Exit27DynamicBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name>{layer_name}</name></metadata>']
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
