# Exit 27 Unsanctioned Freeride Network

A comprehensive geospatial dataset and regulatory audit of the underground mountain bike trail network at **Exit 27** on the western shoulder of Rattlesnake Mountain, adjacent to the Raging River State Forest (King County, WA).

---

## Datasets & Exact API Specifications

The Exit 27 network was mapped and audited by cross-referencing five primary data sources:

| Dataset / Source | Exact API Endpoint / Spatial Identifier | Purpose in Analysis |
| :--- | :--- | :--- |
| **OpenStreetMap Core API 0.6** | `https://api.openstreetmap.org/api/0.6/map?bbox=-121.8750,47.4650,-121.8150,47.5050` | Raw way coordinates, node elevations, surface materials, and trail tags. |
| **King County Cadastral GIS** | Parcel PIN `1423089001` (Rattlesnake Mountain NRCA) | Evaluating RCW 79.71 state ecological conservation boundary violations. |
| **WA DNR Transportation Baseline** | WA DNR Public Forest Practices GIS Portal | Differentiating authorized logging spurs from rogue trail singletracks. |
| **EMBA / WA DNR Corridor Data** | Raging River State Forest Engineering Corridors | Identifying unauthorized bypass incursions along the *Return Policy* climbing trail. |
| **Trailforks Regional Directory** | Raging River / Exit 27 Unofficial Freeride Roster | Community consensus names, historical video archives, and difficulty ratings. |

---

## Trail Naming Derivation Methodology

Consistent with the master repository standard, every trail in Exit 27 carries a 100% clean community name with zero prefix clutter:

1. **Established Builder & Community Names:** Major gravity descents retain their historic names verified across local riding communities:
   * *Bruce Willis*, *Balls Deep*, *Oregon*, *Loam Star*, *Coal Train*, *Mainline*, *Missionary*, *Supernatural*, *LSD*, *Lochsa*, *Belly Dance*.
2. **Resolution of Unnamed Segments (Local Community Consensus):** Formerly unnamed or generic connectors were cross-referenced against local builder logs and resolved to their authentic community designations:
   * *B-Line* (OSM Way `1371077864`)
   * *Dingleberry* (OSM Way `1371077852`)
   * *Smoke Break* (OSM Way `1371077861`)
3. **Topological Continuity for Connecting Links:** Minor link lines, alternate drops, and bypasses lacking separate historic names inherit their name from the parent trail they connect:
   * *Return Policy Bypass North* (OSM Way `1286010808`)
   * *Return Policy Bypass South* (OSM Way `1286010809`)
   * *Mainline Connector East/West* (OSM Ways `1371077863` / `1371077862`)
   * *Coal Train Link* (OSM Way `1371077860`)
   * *B-Line North/South Links* (OSM Ways `1371077865` / `1371077866`)
4. **Historical Physical Demolitions:** The decommissioned singletrack demolished during DNR logging operations is named *Demolished Singletrack* (OSM Way `1286010811`).

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

The dataset isolates **52 unsanctioned trail segments** totaling **23.14 km** of singletrack:

| Category | Hex Color | Visual Indicator | Criteria | Trail Count |
| :--- | :--- | :--- | :--- | :--- |
| **WILL BE Decommissioned** | `#ea580c` | **Blaze Orange** | Active DNR decommissioning targets violating NRCA boundary or Return Policy buffer. | 5 trails |
| **ALREADY Decommissioned** | `#475569` | **Ghost Slate** | Physically demolished lines (dragged brush, felled timber, obliterated tread). | 1 trail |
| **Active Freeride (Double Black)** | `#000000` | **Solid Black** | Extreme gravity lines with steep pitches (>25%), gap jumps, and mandatory drops. | 28 trails |
| **Active Freeride (Black Diamond)** | `#dc2626` | **Crimson Red** | Advanced technical singletrack descents, root webs, and off-camber loam. | 18 trails |

---

## Reproducible Build Script

The complete pipeline to re-query the APIs, audit the boundaries, resolve names, and regenerate all vector formats is provided in the local `scripts/` directory:

```bash
# From within this directory:
python scripts/build_exit27.py
```

### Script Manifest:
* **[`scripts/build_exit27.py`](./scripts/build_exit27.py):** Standalone Python script that queries the OpenStreetMap Core API bbox, applies the King County PIN and Return Policy exclusion filters, executes Option A naming, and exports the master and separated GeoJSON, KML 2.2, and GPX 1.1 layers.

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
