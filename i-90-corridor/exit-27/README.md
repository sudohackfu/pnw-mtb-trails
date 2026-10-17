# Exit 27 Unsanctioned Freeride Network

A comprehensive geospatial dataset and regulatory audit of the underground mountain bike trail network at **Exit 27** on the western shoulder of Rattlesnake Mountain, adjacent to the Raging River State Forest (King County, WA).

---

## Sources & Data Provenance

The Exit 27 network was mapped and audited by cross-referencing five primary data sources:
1. **Physical Trail Geometries:** OpenStreetMap (OSM) Core API 0.6 and Overpass API multi-tile extractions covering bounding coordinates `47.4650°N to 47.5050°N` and `-121.8750°W to -121.8150°W`.
2. **King County Cadastral GIS:** King County Department of Assessments parcel boundary geodatabase, isolating Parcel PIN `1423089001` (Rattlesnake Mountain Natural Resources Conservation Area).
3. **WA DNR Public Forest Practices Transportation Layer:** Washington State Department of Natural Resources official GIS dataset for authorized forest roads, logging spurs, and officially recognized trail easements.
4. **Evergreen Mountain Bike Alliance (EMBA) & WA DNR Baselines:** Official engineering corridors for the sanctioned Raging River State Forest system, specifically the *Return Policy* climbing trail corridor.
5. **Community Ground-Truth & Builder Lore:** Local rider GPS logs, Trailforks historical records, and Strava heatmaps confirming active maintenance, physical tread wear, and underground trail naming conventions.

---

## Trail Naming Derivation Methodology

Consistent with the master repository standard, every trail in Exit 27 carries a 100% clean community name with zero prefix clutter. Names were derived through a 3-step resolution process:

1. **Established Builder & Community Names:** Major gravity descents retain their historic names verified across local riding communities and video archives:
   * *Bruce Willis*, *Balls Deep*, *Oregon*, *Loam Star*, *Coal Train*, *Mainline*, *Missionary*, *Supernatural*, *LSD*, *Lochsa*, *Belly Dance*.
2. **Resolution of Unnamed Segments (Local Community Consensus):** Formerly unnamed or generic connectors were cross-referenced against local builder logs and resolved to their authentic community designations:
   * *B-Line* (Way `1371077864`)
   * *Dingleberry* (Way `1371077852`)
   * *Smoke Break* (Way `1371077861`)
3. **Topological Continuity for Connecting Links:** Minor link lines, alternate drops, and bypasses lacking separate historic names inherit their name from the parent trail they connect:
   * *Return Policy Bypass North* (Way `1286010808`)
   * *Return Policy Bypass South* (Way `1286010809`)
   * *Mainline Connector East/West*
   * *Coal Train Link*
4. **Historical Physical Demolitions:** The decommissioned singletrack demolished during DNR logging operations is named *Demolished Singletrack* (Way `1286010811`).

---

## Regulatory Context & Boundary Audits

Portions of this network intersect sensitive public land conservation boundaries, triggering active and pending decommissioning efforts by the Washington State Department of Natural Resources (WA DNR):

1. **Rattlesnake Mountain NRCA (RCW 79.71):**
   * **Boundary:** King County Parcel PIN `1423089001`.
   * **Legal Mandate:** Natural Resources Conservation Areas are managed under Washington state law strictly for ecological preservation and low-impact nature study; bicycle trail construction is prohibited by law.
   * **Action:** Trails penetrating this eastern boundary (*Deer*, *Cougar*, *Elk*) are targeted for full physical decommissioning.
2. **Return Policy Climbing Corridor Buffer:**
   * Unsanctioned bypass lines running parallel to or intersecting the sanctioned **Return Policy** climbing corridor (*Return Policy Bypass North*, *Return Policy Bypass South*) are flagged for removal to prevent erosion, corridor braidedness, and head-on collisions between descending freeriders and climbing multi-use traffic.

---

## Trail Inventory & Status Classification

The dataset isolates **52 unsanctioned trail segments** totaling **23.14 km** of singletrack. Status and difficulty are conveyed strictly via vector styling.

### Status & Color Legend

| Category | Hex Color | Visual Indicator | Criteria | Trail Count |
| :--- | :--- | :--- | :--- | :--- |
| **WILL BE Decommissioned** | `#ea580c` | **Blaze Orange** | Active DNR decommissioning targets violating NRCA boundary or Return Policy buffer. | 5 trails |
| **ALREADY Decommissioned** | `#475569` | **Ghost Slate** | Physically demolished lines (dragged brush, felled timber, obliterated tread). | 1 trail |
| **Active Freeride (Double Black)** | `#000000` | **Solid Black** | Extreme gravity lines with steep pitches (>25%), gap jumps, and mandatory drops. | 28 trails |
| **Active Freeride (Black Diamond)** | `#dc2626` | **Crimson Red** | Advanced technical singletrack descents, root webs, and off-camber loam. | 18 trails |

### Trail Roster Highlights

* **DNR Decommissioning Targets (`#ea580c` Blaze Orange):**
  * *Return Policy Bypass North*
  * *Return Policy Bypass South*
  * *Deer*
  * *Cougar*
  * *Elk*
* **Already Demolished (`#475569` Ghost Slate):**
  * *Demolished Singletrack* (OSM Way `1286010811`)
* **Active Freeride Lines (`#000000` Black / `#dc2626` Red):**
  * *Bruce Willis*, *Balls Deep*, *Oregon*, *Loam Star*, *Coal Train*, *Mainline*, *Missionary*, *Supernatural*, *LSD*, *Lochsa*, *B-Line*, *Dingleberry*, *Smoke Break*, *Belly Dance*, and associated connecting links.

---

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `exit27_unsanctioned_trails.kml` | KML 2.2 | Pure static vector line placemarks with baked-in hex colors. Compatible with CalTopo, Gaia GPS, and Google Earth. |
| `exit27_unsanctioned_network.geojson` | GeoJSON | Complete WGS84 feature collection including all 57 raw OpenStreetMap tags, length, difficulty, and status metadata. |
| `exit27_unsanctioned_network.gpx` | GPX 1.1 | Combined GPX vector tracks enriched with Trailforks (`<tf:...>`) and Garmin (`<gpxx:...>`) extensions. |
| `exit27_active_freeride.gpx` | GPX 1.1 | Isolated layer of the 46 active freeride trails. |
| `exit27_WILL_BE_decommissioned.gpx` | GPX 1.1 | Isolated layer containing only the 5 trails flagged for pending DNR removal. |
| `exit27_ALREADY_decommissioned.gpx` | GPX 1.1 | Isolated layer containing the physically demolished singletrack line. |
| `decommission_targets.geojson` | GeoJSON | Spatial boundary intersection layer flagging NRCA encroachment. |
| `nrca_boundary.geojson` | GeoJSON | Parcel boundary polygon for King County PIN `1423089001` (Rattlesnake Mountain NRCA). |
| `dnr_authorized.geojson` | GeoJSON | WA DNR Public Forest Practices transportation layer baseline. |
| `exit27_raging_river_master.geojson` | GeoJSON | Unfiltered reference dataset combining sanctioned and unsanctioned lines across the entire corridor. |
| `exit27_raging_river_master.gpx` | GPX 1.1 | Unfiltered reference GPX trackset for the full corridor. |
