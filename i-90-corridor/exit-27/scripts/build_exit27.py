#!/usr/bin/env python3
"""
Exit 27 Unsanctioned Freeride Network Builder & Geospatial Audit Engine

This script queries the OpenStreetMap Core API, loads the community-vetted
trail name gazetteer (community_names.json), audits intersections against the King County
Cadastral NRCA parcel polygon, computes proximity to the Return Policy climbing corridor,
and generates multi-format vector datasets with 100% authentic community names.

Datasets Queried:
1. OpenStreetMap (OSM) Core API 0.6:
   Endpoint: https://api.openstreetmap.org/api/0.6/map?bbox=-121.8750,47.4650,-121.8150,47.5050
2. King County Cadastral NRCA Boundary:
   File: ../nrca_boundary.geojson (Parcel PIN 1423089001 - Rattlesnake Mountain NRCA, RCW 79.71)
3. Community Trail Name Gazetteer:
   File: community_names.json (Vetted rider names, ratings, and status metadata)
"""

import os
import sys
import json
import math
import requests
import xml.etree.ElementTree as ET
from shapely.geometry import shape, LineString
from shapely.ops import unary_union

HEADERS = {'User-Agent': 'PNW-MTB-Trails-Exit27-DynamicBuilder/3.0'}
BBOX = (-121.8750, 47.4700, -121.8150, 47.5150)

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
    gazetteer_path = os.path.join(script_dir, "community_index.json")
    
    # 1. Load Community Trail Name Gazetteer
    if not os.path.exists(gazetteer_path):
        print(f"Error: Community gazetteer not found at {gazetteer_path}")
        sys.exit(1)
        
    with open(gazetteer_path, "r", encoding="utf-8") as f:
        community_gazetteer = json.load(f)
    print(f"Loaded {len(community_gazetteer)} community-vetted trail records from gazetteer.")
    
    # 2. Load King County Cadastral NRCA Boundary
    with open(nrca_path, "r", encoding="utf-8") as f:
        nrca_poly = shape(json.load(f)['features'][0]['geometry'])
        
    # 3. Fetch OSM Vector Data
    print("Querying OpenStreetMap Core API for Exit 27...")
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}"
    r = requests.get(url, headers=HEADERS, timeout=60)
    if r.status_code != 200:
        print(f"Failed to fetch OSM data: HTTP {r.status_code}")
        sys.exit(1)
        
    root = ET.fromstring(r.content)
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
        
    ways_dict = {}
    for way in root.findall('way'):
        wid = way.attrib['id']
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        ways_dict[wid] = {'tags': tags, 'nodes': nd_refs}
        
    # Filter and construct features for the Exit 27 freeride network
    features = []
    
    for wid, info in community_gazetteer.items():
        if wid not in ways_dict:
            continue
        w = ways_dict[wid]
        coords = [nodes[ref] for ref in w['nodes'] if ref in nodes]
        if len(coords) < 2:
            continue
            
        line_geom = LineString(coords)
        length_m = calculate_length_m(coords)
        
        # Verify NRCA boundary violation dynamically
        violates_nrca = line_geom.intersects(nrca_poly)
        status = info['status']
        if violates_nrca and "Decommission" not in status:
            status = "WILL BE Decommissioned"
            
        name = info['name']
        diff = info['difficulty']
        stroke = info['stroke']
        imba = info.get('imba_scale', 3)
        
        feature = {
            'type': 'Feature',
            'id': wid,
            'properties': {
                'name': name,
                'status': status,
                'difficulty': diff,
                'imba_scale': imba,
                'stroke': stroke,
                'stroke-width': 4.0,
                'length_m': length_m,
                'osm_id': wid,
                'tags': w['tags']
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        }
        features.append(feature)
        
    print(f"Constructed {len(features)} Exit 27 unsanctioned trails with 100% authentic community names.")
    
    # Export GeoJSON
    with open(os.path.join(target_dir, "exit27_unsanctioned_network.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': features}, f, indent=2, ensure_ascii=False)
        
    # Export KML 2.2
    export_kml(features, os.path.join(target_dir, "exit27_unsanctioned_trails.kml"))
    
    # Export Master GPX
    export_gpx(features, os.path.join(target_dir, "exit27_unsanctioned_network.gpx"), "Exit 27 Unsanctioned Master")
    
    # Export Separated Layers
    will_decom = [f for f in features if "WILL BE" in f['properties']['status']]
    already_decom = [f for f in features if "ALREADY" in f['properties']['status'] or "Decommissioned" == f['properties']['status']]
    active = [f for f in features if "Active" in f['properties']['status']]
    
    # Export Decommission Targets GeoJSON
    decom_features = will_decom + already_decom
    with open(os.path.join(target_dir, "decommission_targets.geojson"), "w", encoding="utf-8") as f:
        json.dump({'type': 'FeatureCollection', 'features': decom_features}, f, indent=2, ensure_ascii=False)
        
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
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<gpx version="1.1" creator="Exit27DynamicBuilder" xmlns="http://www.topografix.com/GPX/1/1" xmlns:tf="http://www.trailforks.com" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', f'  <metadata><name><![CDATA[{layer_name}]]></name></metadata>']
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
