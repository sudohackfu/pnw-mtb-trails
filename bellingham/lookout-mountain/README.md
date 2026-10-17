# Lookout Mountain & Lake Whatcom Networks

A comprehensive geospatial dataset of the mountain bike singletrack trails across **Lookout Mountain Forest Preserve**, **Lake Whatcom Park**, and **Stewart Mountain** (Whatcom County, WA).

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Two sub-quadrant bboxes:<br>1. Lookout Mountain: (-122.380, 48.690, -122.310, 48.770)<br>2. Stewart Mountain / Lake Whatcom: (-122.320, 48.720, -122.240, 48.780) | Way geometry, node elevations, surface materials, and trail tags. |
| **Whatcom County Parks Master Plan** | Whatcom County Parks & Recreation GIS Portal | Park boundaries, sanctioned singletrack alignments, and Stimpson Nature Reserve borders. |
| **WA DNR Olsen Creek Block GIS** | WA DNR Forest Practices GIS Portal | State forest non-motorized recreation corridors. |
| **Community Trail Index** | [scripts/community_index.json](./scripts/community_index.json) | Vetted rider names (*#5, #8, BR*), difficulty ratings, and research sources. |

---

## Land Management & Historical Context

Situated along the eastern flank of Lake Whatcom, this network spans county park preserve lands and state timber:
* **Lookout Mountain Forest Preserve:** Managed by **Whatcom County Parks & Recreation**. Features modern gravity descents (*Cougar Ridge, Floam*) built to relieve trail pressure on Galbraith.
* **Lake Whatcom Park & Stewart Mountain:** Features long sustained climbs and descents (*Chanterelle, Brown Pow*). Historically, Stewart Mountain hosted underground rogue freeride tracks, some of which were adopted by the county while others were decommissioned.
* **Stimpson Family Nature Reserve (Conservation Boundary):** Directly adjacent to Lookout Mountain, this 350-acre reserve is strictly preserved for wildlife habitat; **all bicycle access is prohibited by county code**.

---

## Trail Naming Derivation & Governance Architecture

We implement a strict **Programmatic First -> Manual Review & Triage -> External Research -> Community Index Override** pipeline:

`
[ OSM Live API Query ]
         |
         v
[ Fire Road & Pedestrian Filter ] (excludes OC-17, Seed Orchard Rd, Stimpson Reserve bicycle=no)
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

1. **Programmatic First:** Official park singletracks are parsed dynamically from OSM tags.
2. **Community Index Override (community_index.json):** Unsanctioned and pirate lines with missing or generic names are researched against builder lore and historical archives. Vetted entries are flagged with "override": true, explicit reasons, and citation sources.
3. **Exclusion of Unverified Placeholders:** Candidate spurs under review ("override": false) that lack verified names are excluded from export so zero generic IDs (Timber Singletrack) reach the published maps.

---

## Trail Inventory & Difficulty Breakdown

* **Total Exported Singletracks:** 74 segments
* **Sanctioned MTB Singletracks:** 61 segments
* **Unsanctioned MTB Singletracks:** 13 segments (100% authentic community names)
* **Candidate Spurs Excluded Under Review:** 63 unverified segments
* **Gravel Fire Roads / Service Doubletracks:** Filtered out (OC-ML, OC-17, Seed Orchard Road)
* **Pedestrian Footpaths Excluded (icycle=no):** *Stimpson Main Loop*, *Strawberry Falls Trail*, *Leila June Trail*, *Geneva Pond Loop*

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Black Diamond** | Level 3 | #dc2626 | 4 segments | *Cougar Ridge Trail, Floam, Brown Pow* |
| **Blue Square** | Level 2 | #0284c7 | 49 segments | *Rufus Creek Trail, Chanterelle Trail, El Diablo, Moto's Run, Bottoms Up, Hooty Hoot, Waterfall Trail (Gnargus), Earth Star, Turkey Tail, Baneberry Trail* |
| **Green Circle** | Level 1 | #22c55e | 8 segments | *Creekside Trail, Lake Louise Road Connector, Backside Trail links* |

### Vetted Unsanctioned Freeride Roster (#ea580c Orange / #475569 Slate)

* *#5* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; #ea580c)
* *#8* (Stewart Mountain user-maintained singletrack; Level 3 Black Diamond; #ea580c)
* *#5 Link* (Singletrack connector to #5; Level 1 Green Circle; #22c55e)
* *#8 Link* (Singletrack connector to #8; Level 3 Black Diamond; #ea580c)
* *BR* (Historical abandoned / decommissioned singletrack; Level 2 Blue Square; #475569)
* *Hooty Hoot Link* (Technical connector singletrack; Level 3 Black Diamond; #ea580c)
* *Lower Waterfall Link* (Technical singletrack bypass; Level 3 Black Diamond; #ea580c)
* *Bear's Head Link* (Upper Stewart Mountain singletrack; Level 2 Blue Square; #0284c7)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM API, apply singletrack isolation, query community_index.json, and export vector layers is located in scripts/:

`ash
# From within this directory:
python scripts/build_lookout.py
`

### Script Manifest:
* **[scripts/build_lookout.py](./scripts/build_lookout.py):** Standalone Python script that queries the Lookout and Stewart Mountain bounding boxes, applies singletrack filters, resolves overrides from community_index.json, and generates vector datasets.
* **[scripts/community_index.json](./scripts/community_index.json):** The community trail index containing vetted names, difficulty ratings, status flags, and research sources.

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| lookout_sanctioned.geojson | GeoJSON | Complete WGS84 feature collection of the 61 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| lookout_sanctioned.kml | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| lookout_sanctioned.gpx | GPX 1.1 | Vector tracks enriched with <tf:difficulty> and <gpxx:DisplayColor> tags. |
| lookout_unsanctioned.geojson | GeoJSON | Vector feature collection of the 13 verified unsanctioned singletracks. |
| lookout_unsanctioned.kml | KML 2.2 | Styled KML placemarks in Blaze Orange (#ea580c) and Ghost Slate (#475569). |
| lookout_unsanctioned.gpx | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
