# Chuckanut Mountain & Blanchard State Forest

A standardized, multi-source geospatial repository and regulatory inventory of the seaside mountain bike singletracks across **Chuckanut Mountain** and **Blanchard State Forest** (Whatcom & Skagit Counties, WA).

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Bounding box: (-122.520, 48.600, -122.420, 48.700) | Way geometry, node coordinates, surface materials, and trail tags. |
| **WA DNR Blanchard Recreation Plan** | WA DNR Forest Practices GIS Portal | Blanchard State Forest authorized non-motorized trail network. |
| **Washington State Parks GIS** | Larrabee State Park Boundary & Facility Inventory | Auditing pedestrian-only conservation restrictions (icycle=no). |
| **Community Trail Index** | [scripts/community_index.json](./scripts/community_index.json) | Vetted rider names, difficulty ratings, and external research sources. |

---

## Land Management & Regulatory Context

Rising directly from the saltwater shoreline of Samish Bay, Chuckanut and Blanchard Mountains feature steep sandstone terrain managed under mixed jurisdictions:
* **Larrabee State Park:** Managed by the **Washington State Parks and Recreation Commission**. Features strict enforcement against mountain bikes on pedestrian-only conservation footpaths.
* **Blanchard State Forest:** Managed by the **Washington State Department of Natural Resources (WA DNR)**. Hosts officially sanctioned technical gravity descents (*Double Black Diamond, Double Down*).
* **Chuckanut Mountain Park:** Managed by **Whatcom County Parks & Recreation**.

---

## Trail Naming Derivation & Governance Architecture

We implement a strict **Programmatic First -> Manual Review & Triage -> External Research -> Community Index Override** pipeline:

`
[ OSM Live API Query ]
         |
         v
[ Fire Road & Pedestrian Filter ] (excludes Cleator Rd, Fragrance Lake Rd, BL-1616, bicycle=no)
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

1. **Programmatic First:** High-trust public API metadata is parsed automatically without hardcoded logic in the Python builder.
2. **Community Index Override (community_index.json):** Unsanctioned and pirate lines with missing or generic names are researched against builder lore, Strava segment leaderboards, and historical records. Vetted entries are flagged with "override": true, explicit reasons, and citation sources.
3. **Exclusion of Unverified Placeholders:** Candidate spurs under review ("override": false) that lack verified names are excluded from export so zero generic IDs (Pirate Singletrack) reach the published maps.

---

## Trail Inventory & Difficulty Breakdown

* **Total Exported Singletracks:** 109 segments
* **Sanctioned MTB Singletracks:** 96 segments
* **Unsanctioned MTB Singletracks:** 13 segments (100% authentic community names)
* **Candidate Spurs Excluded Under Review:** 70 unverified segments
* **Logging Roads & Fire Roads Filtered Out:** BL-1616, DNR B-1600, Cleator Road, Fragrance Lake Road, Lost Lake Road, Pacific Rim Drive
* **Pedestrian Footpaths Excluded (icycle=no):** *Rock Trail*, *Fragrance Lake Cliff Trail*, *Chinscraper*, *Teddy Bear Cove Trail*

### Sanctioned Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Double Black** | Level 4 | #000000 | 2 segments | *Double Down, The Horn* |
| **Black Diamond** | Level 3 | #dc2626 | 13 segments | *Double Black Diamond (DBD), Hush Hush Trail, Madrone Crest Trail, Ridge Trail* |
| **Blue Square** | Level 2 | #0284c7 | 68 segments | *Dan's Traverse Trail, Hemlock Trail, Cinco, Raptor Ridge, Salal Trail, Fern Trail, Lost Lake links* |
| **Green Circle** | Level 1 | #22c55e | 13 segments | *Clayton Beach Trail, Interurban Trail links* |

### Vetted Unsanctioned Freeride Roster (#ea580c Blaze Orange)

* *Fiona Ridge* (Exposed rocky cliffline singletrack; Level 3 Black Diamond)
* *Rooty Ridge* (Dense root-carpet technical descent; Level 3 Black Diamond)
* *Rooty Ridge Lower* (Steep fall-line loam chute; Level 3 Black Diamond)
* *Pine and Cedar Lakes Trail Link* (Community connector network; Level 3 Black Diamond)
* *Upper Bluff Trail Link* (Sandstone bluff technical link; Level 3 Black Diamond)
* *Salal Trail Link* (Loamy ridge traverse bypass; Level 3 Black Diamond)
* *Fragrance Lake Trail Link* (High-clearance bypass connector; Level 3 Black Diamond)
* *Interurban Trail Link* (Low-elevation connector; Level 3 Black Diamond)

---

## Reproducible Build Script

The complete pipeline to re-query the OSM API, apply singletrack isolation, query community_index.json, and export vector layers is located in scripts/:

`ash
# From within this directory:
python scripts/build_chuckanut.py
`

### Script Manifest:
* **[scripts/build_chuckanut.py](./scripts/build_chuckanut.py):** Standalone Python script that queries the Chuckanut bounding box, applies the singletrack filter, resolves overrides from community_index.json, and generates vector datasets.
* **[scripts/community_index.json](./scripts/community_index.json):** The community trail index containing vetted names, difficulty ratings, status flags, and research sources.

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| chuckanut_sanctioned.geojson | GeoJSON | Complete WGS84 feature collection of the 96 sanctioned singletracks with IMBA ratings, lengths, and tags. |
| chuckanut_sanctioned.kml | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| chuckanut_sanctioned.gpx | GPX 1.1 | Vector tracks enriched with <tf:difficulty> and <gpxx:DisplayColor> tags. |
| chuckanut_unsanctioned.geojson | GeoJSON | Vector feature collection of the 13 verified unsanctioned singletracks. |
| chuckanut_unsanctioned.kml | KML 2.2 | Styled KML placemarks in Blaze Orange (#ea580c). |
| chuckanut_unsanctioned.gpx | GPX 1.1 | Unsanctioned tracks for offline GPS navigation. |
