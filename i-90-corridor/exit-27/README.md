# Exit 27 Unsanctioned Freeride Network

A comprehensive geospatial dataset and regulatory audit of the underground mountain bike trail network at **Exit 27** on the western flank of Rattlesnake Mountain, adjacent to the Raging River State Forest (King County, WA).

## Overview

Exit 27 is one of the most historically renowned freeride and downhill zones in the Pacific Northwest. Characterized by 1,800 to 2,200 vertical feet of continuous descent, the network features steep organic loam, high-consequence wooden gap jumps, rock drops, and road gaps accessed via DNR logging spurs off Interstate 90.

Unlike the officially developed trails in the adjacent Raging River State Forest, the Exit 27 network is entirely unsanctioned and maintained by underground volunteer builders.

## Regulatory Context & Geospatial Audits

Portions of this network intersect sensitive public land conservation boundaries, triggering active and pending decommissioning efforts by the Washington State Department of Natural Resources (WA DNR):

1. **Rattlesnake Mountain NRCA (RCW 79.71):**
   * **Boundary:** King County Parcel PIN `1423089001`.
   * **Mandate:** Natural Resources Conservation Areas are managed under Washington state law for ecological preservation; bicycle trail development is strictly prohibited. Trails crossing this eastern boundary line are designated for physical decommissioning.
2. **Authorized Trail Buffers:**
   * Unsanctioned lines running parallel to or intersecting the sanctioned **Return Policy** climbing corridor are targeted to prevent user confusion, erosion, and conflicts.

## Trail Inventory & Status Classification

The dataset isolates **52 unsanctioned trail segments** totaling **23.14 km** of singletrack. All trails use 100% pure community names without prefix clutter; status and difficulty are conveyed strictly via vector styling.

### Status & Color Legend

| Category | Hex Color | Visual Indicator | Description | Trail Count |
| :--- | :--- | :--- | :--- | :--- |
| **WILL BE Decommissioned** | `#ea580c` | **Blaze Orange** | Active DNR decommissioning targets violating NRCA boundary or Return Policy buffer. | 5 trails |
| **ALREADY Decommissioned** | `#475569` | **Ghost Slate** | Physically demolished lines (dragged brush, felled timber, obliterated tread). | 1 trail |
| **Active Freeride (Double Black)** | `#000000` | **Solid Black** | Active unsanctioned gravity lines with extreme features, steep pitches, and gap jumps. | 28 trails |
| **Active Freeride (Black Diamond)** | `#dc2626` | **Crimson Red** | Active advanced singletrack descents, technical loam, and rock gardens. | 18 trails |

### Trail Roster Highlights

* **DNR Decommissioning Targets (`#ea580c` Blaze Orange):**
  * *Return Policy Bypass North*
  * *Return Policy Bypass South*
  * *Deer*
  * *Cougar*
  * *Elk*
* **Already Demolished (`#475569` Ghost Slate):**
  * *Demolished Singletrack* (Way `1286010811`)
* **Active Freeride Lines (`#000000` Black / `#dc2626` Red):**
  * *Bruce Willis*, *Balls Deep*, *Oregon*, *Loam Star*, *Coal Train*, *Mainline*, *Missionary*, *Supernatural*, *LSD*, *Lochsa*, *B-Line*, *Dingleberry*, *Smoke Break*, *Belly Dance*, and associated connecting links.

## File Manifest

| Filename | Format | Description |
| :--- | :--- | :--- |
| `exit27_unsanctioned_trails.kml` | KML 2.2 | Pure static vector line placemarks with baked-in hex colors. Compatible with CalTopo, Gaia GPS, and Google Earth. |
| `exit27_unsanctioned_network.geojson` | GeoJSON | Complete WGS84 feature collection including all 57 raw OpenStreetMap tags, length, difficulty, and status metadata. |
| `exit27_unsanctioned_network.gpx` | GPX 1.1 | Combined GPX vector tracks enriched with Trailforks (`<tf:...>`) and Garmin (`<gpxx:...>`) extensions. |
| `exit27_WILL_BE_decommissioned.gpx` | GPX 1.1 | Isolated layer containing only the 5 trails flagged for pending DNR removal. |
| `exit27_ALREADY_decommissioned.gpx` | GPX 1.1 | Isolated layer containing the physically demolished singletrack line. |
| `exit27_active_freeride.gpx` | GPX 1.1 | Isolated layer of the 46 active freeride trails. |
| `decommission_targets.geojson` | GeoJSON | Spatial boundary intersection layer flagging NRCA encroachment. |
| `nrca_boundary.geojson` | GeoJSON | Parcel boundary polygon for King County PIN `1423089001` (Rattlesnake Mountain NRCA). |
| `dnr_authorized.geojson` | GeoJSON | WA DNR Public Forest Practices transportation layer baseline. |
| `exit27_raging_river_master.geojson` | GeoJSON | Unfiltered reference dataset combining sanctioned and unsanctioned lines across the entire corridor. |
| `exit27_raging_river_master.gpx` | GPX 1.1 | Unfiltered reference GPX trackset for the full corridor. |
