# Galbraith Mountain Trail Network

A definitive geospatial dataset of the mountain bike singletrack trails on **Galbraith Mountain** (Bellingham, WA), spanning both the North (Birch Street / Pipeline) and South (Samish Way / Galbraith Lane) sectors.

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Four sub-quadrant bboxes:<br>1. `(-122.450, 48.695, -122.415, 48.730)`<br>2. `(-122.415, 48.695, -122.380, 48.730)`<br>3. `(-122.450, 48.730, -122.415, 48.760)`<br>4. `(-122.415, 48.730, -122.380, 48.760)` | Way geometries, node elevations, surface materials, and IMBA ratings. |
| **Recreation Easement Baseline** | Whatcom County Auditor File Nos. `2018-0803004` & `2018-0807005` | 2,182-acre Galbraith Tree Farm recreation easement boundary. |
| **WMBC Official Trail Roster** | Whatcom Mountain Bike Coalition Trail Directory | Official trail names, difficulty tiers, and directional downhill flow rules. |
| **City of Bellingham CityIQ GIS** | City of Bellingham Open GIS Portal | Tax parcels and watershed conservation buffers. |
| **Trailforks Region 431** | Trailforks Galbraith Mountain Directory | Secondary line verification and community ride condition reports. |

---

## Land Management & Historical Context

Galbraith Mountain is one of the world's most famous community-managed mountain bike networks. Originally developed as an underground pirate network in the 1980s by the WHIMPS (Whatcom Independent Mountain Pedalers) on active commercial timberland, the network underwent formal legalization:
* **The 2018 Recreation Easement:** In July 2018, the City of Bellingham, Whatcom Land Trust, and the Whatcom Mountain Bike Coalition (WMBC) secured a permanent public recreation easement covering **2,182 acres** of working forest owned by *Galbraith Tree Farm, LLC* (Whatcom County Auditor File Nos. 2018-0803004 / 2018-0807005).
* **Stewardship:** The trail network is built, maintained, and operated through a cooperative agreement with the **WMBC**.
* **Access Policy:** Non-motorized recreation (hiking, running, horseback riding, mountain biking, and Class 1 e-bikes) is legally protected. Commercial timber harvesting continues sustainably across the mountain.

---

## Trail Naming Derivation Methodology

Trail names in this dataset follow the master naming rules established in the repository root:
1. **Primary Ground-Truth Names:** 100% pure official names matching physical on-trail signage installed by WMBC:
   * *Blue Steel*, *Unemployment Line*, *Mohawk*, *Mullet*, *Evolution*, *SST*, *Scorpion*, *Atomic Dog*, *Air Chair*, *Bandito*, *Double Vision*, *Devilcross*, *Irish Death*, *Dad Bod*.
2. **Progression Complexes:** Jump and drop progression tracks carry their explicit feature tiers:
   * *Cedar Dust Green, Blue, Black, and Pro Jump Lines*
   * *Cedar Dust Green, Blue, and Black Drop Lines*
3. **Unsanctioned / Abandoned Lines:** Historic decommissioned lines or off-easement timber tracks retain their community designations (*Old Keystone*, *Scorpion (old)*, *Coyote Ripp*, *Private Trail*). Unnamed informal singletrack cuts are referenced cleanly by their topological OSM Way ID (e.g., *Unnamed Trail (1309122610)*).

---

## Trail Inventory & Difficulty Breakdown

* **Total Singletrack Segments:** 323
* **Sanctioned MTB Singletracks:** 300 segments (222 unique trail names)
* **Unsanctioned MTB Singletracks:** 23 segments (22 unique lines)
* **Gravel Fire Roads / Logging Spurs:** 14 segments filtered out (`RD 2000` series, `Pipeline Road`, `Tower Road`).

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Signature Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Pro-Line** | Level 5 | `#8b5cf6` | 1 segment | ***Blue Steel*** (Fest-series jump line; 40-ft gaps, shark fins) |
| **Double Black** | Level 4 | `#000000` | 3 segments | *Mohawk Pro Line, Cedar Dust Pro Jump Line, Grasshopper* |
| **Black Diamond** | Level 3 | `#dc2626` | 24 segments | *Evolution, Mohawk, Scorpion, Devilcross, Irish Death, Cedar Fever, Dad Bod, Happy Hour, Pour Decisions, Radical Dragon* |
| **Blue Square** | Level 2 | `#0284c7` | 208 segments | *Unemployment Line (U-Line), Mullet, Atomic Dog, Air Chair, Bandito, Double Vision, Cedar Dust Blue lines, Kaiser, Ridge Trail* |
| **Green Circle** | Level 1 | `#22c55e` | 64 segments | *Bunny Trails, Cedar Dust Green lines, Lower Whatcom Falls connector links* |

### Unsanctioned Singletrack Roster (`#ea580c` Orange / `#475569` Slate)
* *Old Keystone* (Historical logging bench singletrack; `#475569`)
* *Scorpion (old)* (Original steep fall-line descent before modern reroute; `#475569`)
* *Coyote Ripp* (Off-easement loamy timber line; `#ea580c`)
* *Private Trail* (Private boundary access line; `#ea580c`)
* *19 Unnamed Informal Singletrack Cuts* (User-built cut-throughs, shortcut chutes, and off-map drops)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM quadrants, isolate singletracks, filter fire roads, apply IMBA ratings, and export all vector formats is provided in the local `scripts/` directory:

```bash
# From within this directory:
python scripts/build_galbraith.py
```

### Script Manifest:
* **[`scripts/build_galbraith.py`](./scripts/build_galbraith.py):** Standalone Python script that queries the 4 Galbraith sub-quadrant bboxes, resolves ratings and names, and generates `galbraith_sanctioned` and `galbraith_unsanctioned` (GeoJSON, KML 2.2, GPX 1.1).

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `galbraith_sanctioned.geojson` | GeoJSON | Complete WGS84 feature collection of all 300 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| `galbraith_sanctioned.kml` | KML 2.2 | Vector placemarks styled in Trailforks colors (Green, Blue, Black, Double Black, Pro Purple). |
| `galbraith_sanctioned.gpx` | GPX 1.1 | Vector tracks enriched with `<tf:difficulty>` and `<gpxx:DisplayColor>` extensions. |
| `galbraith_unsanctioned.geojson` | GeoJSON | Vector feature collection of the 23 unsanctioned and historical singletracks. |
| `galbraith_unsanctioned.kml` | KML 2.2 | Styled KML placemarks (Blaze Orange `#ea580c` for active rogue lines; Ghost Slate `#475569` for abandoned lines). |
| `galbraith_unsanctioned.gpx` | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
