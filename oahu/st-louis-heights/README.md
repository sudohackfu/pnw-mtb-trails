# St. Louis Heights & Wa?ahila Ridge Mountain Bike Network

A standardized geospatial dataset and regulatory inventory of the historic gravity and singletrack mountain bike network across **St. Louis Heights**, **Wa?ahila Ridge**, and **Upper M?noa Valley** (Honolulu, O?ahu, Hawai?i).

---

## Datasets & Exact API Specifications

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | Bounding box: (-157.820, 21.285, -157.785, 21.330) | Way geometry, sub-meter node coordinates, surface types, and trail tags. |
| **Hawai?i DLNR State Parks GIS** | Wa?ahila Ridge State Recreation Area Boundary | Auditing park boundaries and pedestrian-only conservation restrictions (icycle=no). |
| **Hawai?i DOFAW / N? Ala Hele** | State Forest Reserve & Trail Inventory | Differentiating state-adopted hiking footpaths from rider-built gravity corridors. |
| **1996 UCI World Cup Archives** | 1996 Grundig/UCI Downhill World Cup Finals Course Map | Historical alignment of the *World Cup* downhill track. |
| **Community Trail Index** | [scripts/community_index.json](./scripts/community_index.json) | Vetted rider names (*World Cup, Ron's, Wedding Crashers, Waterfall*), ratings, and sources. |

---

## Land Management & Historical Context

Rising sharply between M?noa and P?lolo Valleys overlooking Honolulu and Diamond Head, St. Louis Heights is one of the most storied and technical downhill riding zones in the Pacific:
* **The 1996 UCI World Cup Finals:** On September 7, 1996, the Grundig/UCI Mountain Bike World Cup concluded its season with the Downhill Finals carved into the steep, rooty, red-clay ridges of St. Louis Heights / Wa?ahila Ridge. The track remains an iconic testing ground for Hawaii's downhill community.
* **State Jurisdiction (Hawai?i DLNR):** Managed by the **Division of State Parks** and the **Division of Forestry and Wildlife (DOFAW)**. Under Hawai?i Administrative Rules (HAR Title 13, Chapter 130), the official *Wa?ahila Ridge Trail* is designated strictly for hiking (icycle=no).
* **The Underground Freeride Network:** Over the past three decades, local builders and gravity riders have maintained technical downhill singletracks dropping through the upper Norfolk pine forest and eucalyptus groves down toward Dole Street and M?noa Valley.

---

## Trail Naming Derivation & Governance Architecture

We implement the standard **Programmatic First -> Manual Review & Triage -> External Research -> Community Index Override** pipeline:

`
[ OSM Live API Query ]
         |
         v
[ Road, Sidewalk & Pedestrian Filter ] (excludes St. Louis Dr, Peter St, sidewalks, bicycle=no)
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

1. **Programmatic First:** High-trust public trail names (*Seven Bridges Trail, Kalepohaku Lower Trail, Lanipo Ridge Trail*) are parsed automatically.
2. **Community Index Override (community_index.json):** Underground downhill tracks intentionally unlabelled or obfuscated in public APIs are vetted against local rider lore and historical archives:
   * **World Cup (Wa?ahila DH):** The 1996 UCI World Cup downhill race course (Double Black Diamond).
   * **Ron's:** Raw fall-line technical root chute (Black Diamond / Spicy Blue tier).
   * **Wedding Crashers:** Steep bandit singletrack dropping through the mid-slope timber (Black Diamond).
   * **Waterfall:** High-consequence technical descent dropping into the Wai?akeakua stream basin (Black Diamond).
   * **Bravery Rock:** High-consequence rock roll/drop feature at the ridge crest (Double Black Diamond).
3. **Exclusion of Unverified Placeholders:** Candidate spurs under review ("override": false) and urban walkways are excluded from export so zero generic IDs reach the maps.

---

## Research & Provenance Table (Unsanctioned Freeride Lines)

| Way ID | Community Name | Difficulty | Status | Research Sources & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| 544969461 | **World Cup (Waahila DH)** | Double Black Diamond | Unsanctioned (Community Maintained) | 1996 Grundig/UCI Downhill World Cup Finals archives; Local Oahu gravity builder consensus; Strava segment: Technos to Dole |
| 1545490968 | **Ron's** | Black Diamond | Unsanctioned (Community Built) | Local Oahu rider lore & builder archives |
| 1545490972 | **Wedding Crashers** | Black Diamond | Unsanctioned (Community Built) | Local Oahu rider lore & builder archives |
| 547542860 | **Waterfall** | Black Diamond | Unsanctioned (Gravity Line) | Local Oahu gravity community; Upper Manoa drainage logs |
| 544969459 | **Bravery Rock** | Double Black Diamond | Unsanctioned (Feature) | Local rider feature logs; Waahila ridge crest surveys |
| 544969460 | **Kalepohaku Lower Trail** | Black Diamond | Unsanctioned (Community Maintained) | Local trail logs; Na Ala Hele unadopted singletrack inventory |

---

## Trail Inventory & Difficulty Breakdown

* **Total Exported Singletracks:** 20 segments
* **Sanctioned MTB Singletracks:** 0 (all ridge lines are user-maintained on state lands)
* **Unsanctioned MTB Singletracks:** 20 segments (100% authentic names)
* **Candidate Spurs & Sidewalks Excluded:** 143 unverified / urban segments
* **Paved Roads Filtered Out:** St. Louis Drive, Peter Street, Dole Street, Wa?ahila housing roads
* **Pedestrian Footpaths Excluded (icycle=no):** *Wa?ahila Ridge Trail*, *Kolowalu Trail*, *M?noa Cliff Trail*, *Pu?u Pia Trail*

### Singletrack Difficulty Distribution

| Rating Tier | IMBA Scale | Hex Color | Count | Key Trails |
| :--- | :--- | :--- | :--- | :--- |
| **Double Black** | Level 4 | #000000 | 2 segments | *World Cup (Waahila DH), Bravery Rock* |
| **Black Diamond** | Level 3 | #dc2626 | 13 segments | *Ron's, Wedding Crashers, Waterfall, Kalepohaku Lower Trail, Seven Bridges Trail & Connector, Manoa Middle Ridge* |
| **Blue Square** | Level 2 | #0284c7 | 5 segments | *Naniuapo Falls Trail, Manoa Tunnel Trail, Makiki Valley Trail connectors* |

---

## Reproducible Build Script

The complete pipeline to query OSM, apply singletrack isolation, query community_index.json, and export vector layers is located in scripts/:

`ash
# From within this directory:
python scripts/build_st_louis.py
`

### Script Manifest:
* **[scripts/build_st_louis.py](./scripts/build_st_louis.py):** Standalone Python script that queries the St. Louis Heights / Wa?ahila Ridge bounding box, applies singletrack filters, resolves overrides from community_index.json, and generates vector datasets.
* **[scripts/community_index.json](./scripts/community_index.json):** The community trail index containing vetted names, difficulty ratings, status flags, and research sources.

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| st_louis_unsanctioned.geojson | GeoJSON | Complete WGS84 feature collection of the 20 singletracks with IMBA ratings, lengths, and tags. |
| st_louis_unsanctioned.kml | KML 2.2 | Styled KML vector placemarks for CalTopo, Gaia GPS, and Google Earth. |
| st_louis_unsanctioned.gpx | GPX 1.1 | Vector tracks enriched with <tf:difficulty> and <gpxx:DisplayColor> tags for GPS units. |
