# Lookout Mountain & Lake Whatcom Networks

A comprehensive geospatial dataset of the mountain bike singletrack trails across **Lookout Mountain Forest Preserve**, **Lake Whatcom Park**, and **Stewart Mountain** (Whatcom County, WA).

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Two sub-quadrant bboxes:<br>1. Lookout Mountain: `(-122.380, 48.690, -122.310, 48.770)`<br>2. Stewart Mountain / Lake Whatcom: `(-122.320, 48.720, -122.240, 48.780)` | Way geometry, node elevations, surface materials, and trail tags. |
| **Whatcom County Parks Master Plan** | Whatcom County Parks & Recreation GIS Portal | Park boundaries, sanctioned singletrack alignments, and Stimpson Nature Reserve borders. |
| **WA DNR Olsen Creek Block GIS** | WA DNR Forest Practices GIS Portal | State forest non-motorized recreation corridors. |
| **Trailforks Region 17820 & Records** | Lookout Mountain & Lake Whatcom Directories | Community condition logs, underground builder names (*#5, #8*), and difficulty ratings. |

---

## Land Management & Historical Context

Situated along the eastern flank of Lake Whatcom, this network spans county park preserve lands and state timber:
* **Lookout Mountain Forest Preserve:** Managed by **Whatcom County Parks & Recreation**. Features modern, machine-built and hand-finished gravity descents (*Cougar Ridge, Floam*) built to relieve trail pressure on Galbraith.
* **Lake Whatcom Park & Stewart Mountain:** Features long sustained climbs and descents (*Chanterelle, Brown Pow*). Historically, Stewart Mountain hosted underground rogue freeride tracks (*Surfin' Turf, Brown Pow*), some of which were adopted by the county while others were decommissioned.
* **Stimpson Family Nature Reserve (Conservation Boundary):** Directly adjacent to Lookout Mountain, this 350-acre reserve is strictly preserved for wildlife habitat; **all bicycle access is prohibited by county code**.

---

## Trail Naming Derivation Methodology

1. **Official Ground-Truth Singletracks:**
   * *Cougar Ridge Trail*: The premier 1,400-ft descent on Lookout Mountain (fast berms, natural timber flow, technical root carpets).
   * *Floam*: Steep, deep-loam technical descent dropping off the upper ridgeline.
   * *Brown Pow*: The famous descent in Lake Whatcom Park (bermed turns, tabletop jumps, and steep loamy switchbacks).
   * *Rufus Creek Trail (Rufous Creek)*: Sustained technical descent linking the upper logging benches.
   * *Chanterelle Trail, El Diablo, Moto's Run, Bottoms Up, Hooty Hoot, Waterfall Trail (Gnargus), Baneberry Trail, Creekside Trail, Earth Star, Turkey Tail*.
2. **Community-Maintained Pirate Singletracks:**
   * *#5 & #8*: Active, user-maintained dirt singletracks cut through the timber on Stewart Mountain above Lake Whatcom.
   * *BR*: Historical abandoned/unauthorized singletrack line (`#475569`).
   * *18 Unnamed Informal Singletrack Lines*: Rogue cuts and bandit chutes referenced cleanly by their topological OSM Way ID (e.g., *Unnamed Trail (1470422399)*).
3. **Excluded Pedestrian-Only Footpaths:**
   * Official walking trails in the Stimpson Family Nature Reserve where bikes are prohibited (`bicycle=no`) are excluded: *Stimpson Main Loop*, *Strawberry Falls Trail*, *Leila June Trail*, and *Geneva Pond Loop*.

---

## Trail Inventory & Difficulty Breakdown

* **Total Singletrack Segments:** 71
* **Sanctioned MTB Singletracks:** 50 segments (30 unique trail names)
* **Unsanctioned MTB Singletracks:** 21 segments (21 unique lines)
* **Gravel Fire Roads / Service Doubletracks:** 3 segments filtered out (`OC-ML`, `OC-17`, `Seed Orchard Trail`).

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Black Diamond** | Level 3 | `#dc2626` | 4 segments | *Cougar Ridge Trail, Floam, Brown Pow* |
| **Blue Square** | Level 2 | `#0284c7` | 38 segments | *Rufus Creek Trail, Chanterelle Trail, El Diablo, Moto's Run, Bottoms Up, Hooty Hoot, Waterfall Trail (Gnargus), Earth Star, Turkey Tail, Baneberry Trail* |
| **Green Circle** | Level 1 | `#22c55e` | 8 segments | *Creekside Trail, Lake Louise Road Connector, Backside Trail links* |

### Unsanctioned Singletrack Roster (`#ea580c` Orange / `#475569` Slate)
* *#5* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; `#ea580c`)
* *#8* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; `#ea580c`)
* *BR* (Abandoned / decommissioned singletrack; Level 3 Black Diamond; `#475569`)
* *18 Unnamed Informal Singletrack Lines* (Hand-cut timber chutes and bandit bypasses; `#ea580c`)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM data, strip service roads, isolate singletracks, apply ratings, and export all vector formats is provided in the local `scripts/` directory:

```bash
# From within this directory:
python scripts/build_lookout.py
```

### Script Manifest:
* **[`scripts/build_lookout.py`](./scripts/build_lookout.py):** Standalone Python script that queries the Lookout Mountain and Stewart Mountain bounding boxes, applies the Stimpson Reserve exclusion filter, resolves ratings and names, and generates `lookout_sanctioned` and `lookout_unsanctioned` (GeoJSON, KML 2.2, GPX 1.1).

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `lookout_sanctioned.geojson` | GeoJSON | Complete WGS84 feature collection of the 50 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| `lookout_sanctioned.kml` | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| `lookout_sanctioned.gpx` | GPX 1.1 | Vector tracks enriched with `<tf:difficulty>` and `<gpxx:DisplayColor>` tags. |
| `lookout_unsanctioned.geojson` | GeoJSON | Vector feature collection of the 21 unsanctioned and user-maintained singletracks. |
| `lookout_unsanctioned.kml` | KML 2.2 | Styled KML placemarks in Blaze Orange (`#ea580c`) and Ghost Slate (`#475569`). |
| `lookout_unsanctioned.gpx` | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
