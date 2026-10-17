# Galbraith Mountain Trail Network

A definitive geospatial dataset of the mountain bike singletrack trails on **Galbraith Mountain** (Bellingham, WA), spanning both the North (Birch Street / Pipeline) and South (Samish Way / Galbraith Lane) sectors.

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Four sub-quadrant bboxes:<br>1. (-122.450, 48.695, -122.415, 48.730)<br>2. (-122.415, 48.695, -122.380, 48.730)<br>3. (-122.450, 48.730, -122.415, 48.760)<br>4. (-122.415, 48.730, -122.380, 48.760) | Way geometries, node elevations, surface materials, and IMBA ratings. |
| **Recreation Easement Baseline** | Whatcom County Auditor File Nos. 2018-0803004 & 2018-0807005 | 2,182-acre Galbraith Tree Farm recreation easement boundary. |
| **WMBC Official Trail Roster** | Whatcom Mountain Bike Coalition Trail Directory | Official trail names, difficulty tiers, and directional downhill flow rules. |
| **City of Bellingham CityIQ GIS** | City of Bellingham Open GIS Portal | Tax parcels and watershed conservation buffers. |
| **Community Trail Index** | [scripts/community_index.json](./scripts/community_index.json) | Vetted rider names, historical lines (*Old Keystone, Scorpion old*), and research sources. |

---

## Land Management & Historical Context

Galbraith Mountain is one of the world's most famous community-managed mountain bike networks. Originally developed as an underground pirate network in the 1980s by the WHIMPS (Whatcom Independent Mountain Pedalers) on active commercial timberland, the network underwent formal legalization:
* **The 2018 Recreation Easement:** In July 2018, the City of Bellingham, Whatcom Land Trust, and the Whatcom Mountain Bike Coalition (WMBC) secured a permanent public recreation easement covering **2,182 acres** of working forest owned by *Galbraith Tree Farm, LLC* (Whatcom County Auditor File Nos. 2018-0803004 / 2018-0807005).
* **Stewardship:** The trail network is built, maintained, and operated through a cooperative agreement with the **WMBC**.
* **Access Policy:** Non-motorized recreation (hiking, running, horseback riding, mountain biking, and Class 1 e-bikes) is legally protected. Commercial timber harvesting continues sustainably across the mountain.

---

## Trail Naming Derivation & Governance Architecture

We implement a strict **Programmatic First -> Manual Review & Triage -> External Research -> Community Index Override** pipeline:

`
[ OSM Live API Query (4 Quadrants) ]
         |
         v
[ Fire Road & Pedestrian Filter ] (excludes Tower Rd, Pipeline Rd, RD 2000, bicycle=no)
         |
         v
[ Community Index Check ] --(override: true)--> [ Apply Vetted Community Name & Difficulty ]
         | (not overridden)
         v
[ Authentic API Name Present? ] --(yes)--> [ Apply Clean OSM Name ]
         | (no)
         v
[ Topological Link to Named Trail? ] --(yes)--> [ Name as "{Neighbor} Link" ]
         | (no)
         v
[ Unverified Candidate Spur ] --> [ Exclude from Vector Export (Zero Generic Placeholders) ]
`

1. **Programmatic First:** Official recreation easement singletracks are parsed dynamically from live OSM node and way tags.
2. **Community Index Override (community_index.json):** Historical lines and off-easement timber tracks are researched against WMBC historical archives and easement boundary surveys. Vetted entries are flagged with "override": true, explicit reasons, and citation sources.
3. **Exclusion of Unverified Placeholders:** Candidate spurs under review ("override": false) that lack verified names are excluded from export so zero generic IDs (Singletrack) reach the published maps.

---

## Trail Inventory & Difficulty Breakdown

* **Total Exported Singletracks:** 411 segments
* **Sanctioned MTB Singletracks:** 399 segments
* **Unsanctioned MTB Singletracks:** 12 segments (100% authentic community & historical names)
* **Candidate Spurs Excluded Under Review:** 119 unverified segments
* **Gravel Fire Roads / Logging Doubletracks Filtered Out:** RD 2000 series, Pipeline Road, Tower Road, Galbraith Lane
* **Pedestrian Footpaths Excluded (icycle=no):** Footpath access stairs and non-bike easements

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Signature Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Pro-Line** | Level 5 | #8b5cf6 | 1 segment | ***Blue Steel*** (Fest-series jump line; 40-ft gaps, shark fins) |
| **Double Black** | Level 4 | #000000 | 3 segments | *Mohawk Pro Line, Cedar Dust Pro Jump Line, Grasshopper* |
| **Black Diamond** | Level 3 | #dc2626 | 32 segments | *Evolution, Mohawk, Scorpion, Devilcross, Irish Death, Cedar Fever, Dad Bod, Happy Hour, Pour Decisions, Radical Dragon* |
| **Blue Square** | Level 2 | #0284c7 | 275 segments | *Unemployment Line (U-Line), Mullet, Atomic Dog, Air Chair, Bandito, Double Vision, Cedar Dust Blue lines, Kaiser, Ridge Trail* |
| **Green Circle** | Level 1 | #22c55e | 88 segments | *Bunny Trails, Cedar Dust Green lines, Lower Whatcom Falls connector links* |

### Vetted Unsanctioned Freeride Roster (#ea580c Orange / #475569 Slate)

* *Old Keystone* (Historical logging bench singletrack; Level 2 Blue Square; #475569)
* *Scorpion (old)* (Original steep fall-line descent before modern reroute; Level 3 Black Diamond; #475569)
* *Coyote Ripp* (Off-easement loamy timber line; Level 2 Blue Square; #ea580c)
* *Up 2 Something Link* (Technical connector singletrack; Level 2 Blue Square; #ea580c)
* *Boulder Bend Trail Link* (Upper rock slab bypass singletrack; Level 3 Black Diamond; #ea580c)
* *Euclid Trail Link* (Historical western flank singletrack connectors; Level 3 Black Diamond; #ea580c)
* *Hooty Hoot Link* (Off-easement ridge connector; Level 3 Black Diamond; #ea580c)
* *Private Trail* (Private boundary access line; Level 2 Blue Square; #ea580c)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM quadrants, isolate singletracks, query community_index.json, and export vector layers is located in scripts/:

`ash
# From within this directory:
python scripts/build_galbraith.py
`

### Script Manifest:
* **[scripts/build_galbraith.py](./scripts/build_galbraith.py):** Standalone Python script that queries the 4 Galbraith sub-quadrant bboxes, resolves ratings and names, and generates galbraith_sanctioned and galbraith_unsanctioned (GeoJSON, KML 2.2, GPX 1.1).
* **[scripts/community_index.json](./scripts/community_index.json):** The community trail index containing vetted names, difficulty ratings, status flags, and research sources.

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| galbraith_sanctioned.geojson | GeoJSON | Complete WGS84 feature collection of all 399 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| galbraith_sanctioned.kml | KML 2.2 | Vector placemarks styled in Trailforks colors (Green, Blue, Black, Double Black, Pro Purple). |
| galbraith_sanctioned.gpx | GPX 1.1 | Vector tracks enriched with <tf:difficulty> and <gpxx:DisplayColor> extensions. |
| galbraith_unsanctioned.geojson | GeoJSON | Vector feature collection of the 12 unsanctioned and historical singletracks. |
| galbraith_unsanctioned.kml | KML 2.2 | Styled KML placemarks (Blaze Orange #ea580c for active rogue lines; Ghost Slate #475569 for abandoned lines). |
| galbraith_unsanctioned.gpx | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
